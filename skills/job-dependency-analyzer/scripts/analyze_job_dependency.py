#!/usr/bin/env python3
"""
Job Dependency Analyzer - MCP Client

Fetches job dependency information from Zeus MCP and Metadata MCP servers,
builds a dependency graph, and generates Mermaid flowchart for Feishu docs.

Usage:
    python analyze_job_dependency.py --job-ids <job_id1,job_id2,...> [--max-depth N] [--stop-at-tables table1,table2]
"""

import argparse
import json
import requests
import sys
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import deque


@dataclass
class JobInfo:
    """Job information from Zeus MCP"""
    job_id: str
    name: str = ""
    status: str = ""
    run_id: str = ""
    logs: str = ""
    dependencies: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


@dataclass
class TableInfo:
    """Table metadata from Metadata MCP"""
    table_name: str
    source_type: str = ""  # Hive, Iceberg, Paimon, BigQuery, StarRocks
    environment: str = ""
    schema: str = ""
    upstream_jobs: List[str] = field(default_factory=list)


class MCPClient:
    """Client for MCP servers"""
    
    def __init__(self, zeus_url: str, metadata_url: str, token: str):
        self.zeus_url = zeus_url
        self.metadata_url = metadata_url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "x-bbzai-mcp-token": token
        })
        self._zeus_session_id: Optional[str] = None
        self._metadata_session_id: Optional[str] = None
    
    def _initialize_session(self, url: str, server_name: str) -> Optional[str]:
        """Initialize MCP session"""
        try:
            response = self.session.post(url, json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "job-dependency-analyzer", "version": "1.0.0"}
                }
            }, timeout=30)
            
            # Parse SSE response
            content = response.text
            if "data:" in content:
                data_part = content.split("data:")[1].strip()
                result = json.loads(data_part)
                if "result" in result:
                    print(f"[OK] Connected to {server_name} v{result['result'].get('serverInfo', {}).get('version', 'unknown')}")
                    return str(result.get("id", "session-1"))
            return None
        except Exception as e:
            print(f"[WARN] Failed to initialize {server_name}: {e}")
            return None
    
    def _call_tool(self, url: str, tool_name: str, arguments: dict) -> Optional[dict]:
        """Call MCP tool using streamable HTTP transport"""
        try:
            # MCP streamable HTTP requires POST with SSE response
            response = self.session.post(url, json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }, timeout=60, stream=True)
            
            # Parse SSE stream
            content = ""
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    content += line_str + "\n"
                    if line_str.startswith("data:"):
                        data_part = line_str[5:].strip()
                        if data_part:
                            try:
                                result = json.loads(data_part)
                                return result
                            except:
                                continue
            
            # Fallback: try to parse entire response
            if "data:" in content:
                for line in content.split("\n"):
                    if line.startswith("data:"):
                        data_part = line[5:].strip()
                        if data_part:
                            try:
                                result = json.loads(data_part)
                                return result
                            except:
                                continue
            
            return None
        except Exception as e:
            print(f"[ERROR] Tool call failed: {e}")
            return None
    
    def get_job_info(self, job_id: str) -> Optional[JobInfo]:
        """Get job information from Zeus MCP"""
        # Try common tool names for job info
        tool_names = [
            "get_job_info",
            "get_job_details", 
            "query_job",
            "fetch_job",
            "get_job_logs",
            "zeus_get_job"
        ]
        
        for tool_name in tool_names:
            result = self._call_tool(self.zeus_url, tool_name, {"job_id": job_id})
            if result and "result" in result:
                data = result["result"]
                return JobInfo(
                    job_id=job_id,
                    name=data.get("name", data.get("job_name", "")),
                    status=data.get("status", ""),
                    run_id=data.get("run_id", ""),
                    logs=data.get("logs", ""),
                    dependencies=data.get("dependencies", data.get("upstream_jobs", [])),
                    outputs=data.get("outputs", data.get("output_tables", []))
                )
        
        print(f"[WARN] No tool found to fetch job info for {job_id}")
        return JobInfo(job_id=job_id)
    
    def get_table_metadata(self, table_name: str) -> Optional[TableInfo]:
        """Get table metadata from Metadata MCP"""
        tool_names = [
            "get_table_metadata",
            "query_table",
            "get_table_info",
            "fetch_table",
            "metadata_get_table"
        ]
        
        for tool_name in tool_names:
            result = self._call_tool(self.metadata_url, tool_name, {"table_name": table_name})
            if result and "result" in result:
                data = result["result"]
                return TableInfo(
                    table_name=table_name,
                    source_type=data.get("source_type", data.get("type", "")),
                    environment=data.get("environment", data.get("env", "")),
                    schema=data.get("schema", ""),
                    upstream_jobs=data.get("upstream_jobs", data.get("producer_jobs", []))
                )
        
        print(f"[WARN] No tool found to fetch table metadata for {table_name}")
        return TableInfo(table_name=table_name)
    
    def list_tools(self, url: str) -> List[str]:
        """List available tools from MCP server"""
        try:
            response = self.session.post(url, json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }, timeout=30)
            
            content = response.text
            if "data:" in content:
                for line in content.split("\n"):
                    if line.startswith("data:"):
                        data_part = line[5:].strip()
                        if data_part:
                            result = json.loads(data_part)
                            if "result" in result and "tools" in result["result"]:
                                return [t["name"] for t in result["result"]["tools"]]
            return []
        except Exception as e:
            print(f"[ERROR] Failed to list tools: {e}")
            return []


class DependencyGraph:
    """Job dependency graph builder"""
    
    def __init__(self, mcp_client: MCPClient):
        self.client = mcp_client
        self.jobs: Dict[str, JobInfo] = {}
        self.tables: Dict[str, TableInfo] = {}
        self.edges: List[Tuple[str, str, str]] = []  # (from, to, type)
    
    def _is_non_ods_table(self, table_name: str) -> bool:
        """Check if table is non-ODS layer (DWS, ADS, DM, etc.)"""
        # Common non-ODS prefixes
        non_ods_prefixes = ['ads.', 'dws.', 'dm.', 'app.', 'rpt.', 'report.', 'bi.']
        table_lower = table_name.lower()
        return any(prefix in table_lower for prefix in non_ods_prefixes)
    
    def build_graph(self, job_ids: List[str], max_depth: int = 5, 
                    stop_at_tables: Optional[List[str]] = None,
                    downstream: bool = False):
        """Build dependency graph from job IDs
        
        Args:
            job_ids: Starting job IDs
            max_depth: Maximum traversal depth
            stop_at_tables: Tables to stop at
            downstream: If True, trace downstream; if False, trace upstream
        """
        stop_tables = set(stop_at_tables or [])
        visited_jobs: Set[str] = set()
        visited_tables: Set[str] = set()
        queue = deque([(jid, 0) for jid in job_ids])
        
        direction = "downstream" if downstream else "upstream"
        print(f"\n[INFO] Building {direction} dependency graph for {len(job_ids)} job(s)...")
        print(f"[INFO] Max depth: {max_depth}, Stop tables: {stop_tables or 'Non-ODS tables'}")
        
        while queue:
            job_id, depth = queue.popleft()
            
            if job_id in visited_jobs or depth > max_depth:
                continue
            
            visited_jobs.add(job_id)
            print(f"\n[INFO] Fetching job: {job_id} (depth={depth})")
            
            job_info = self.client.get_job_info(job_id)
            if job_info:
                self.jobs[job_id] = job_info
                print(f"  └─ Name: {job_info.name or 'N/A'}, Status: {job_info.status or 'N/A'}")
                
                if downstream:
                    # Trace downstream: find jobs that depend on this job's output tables
                    for table in job_info.outputs:
                        self.edges.append((job_id, f"table:{table}", "produces"))
                        
                        if table in visited_tables:
                            continue
                        visited_tables.add(table)
                        
                        # Check if this is a non-ODS table (stop condition)
                        if self._is_non_ods_table(table):
                            print(f"  └─ 🛑 Non-ODS table (stop): {table}")
                            self.tables[table] = TableInfo(table_name=table, source_type="Unknown")
                            continue
                        
                        # Check stop_at_tables
                        if table in stop_tables or any(st in table for st in stop_tables):
                            print(f"  └─ Stop at table: {table}")
                            continue
                        
                        # Fetch table metadata and find downstream jobs (jobs that use this table)
                        table_info = self.client.get_table_metadata(table)
                        if table_info:
                            self.tables[table] = table_info
                            # downstream_jobs = jobs that read from this table
                            downstream_jobs = table_info.upstream_jobs if hasattr(table_info, 'downstream_jobs') else []
                            if hasattr(table_info, 'downstream_jobs'):
                                downstream_jobs = table_info.downstream_jobs
                            for downstream_job in downstream_jobs:
                                self.edges.append((f"table:{table}", downstream_job, "consumes"))
                                if downstream_job not in visited_jobs:
                                    queue.append((downstream_job, depth + 1))
                else:
                    # Trace upstream (original behavior)
                    for dep_id in job_info.dependencies:
                        self.edges.append((dep_id, job_id, "job_dependency"))
                        if dep_id not in visited_jobs:
                            queue.append((dep_id, depth + 1))
                    
                    for table in job_info.outputs:
                        self.edges.append((job_id, f"table:{table}", "produces"))
                        
                        if table in stop_tables or any(st in table for st in stop_tables):
                            print(f"  └─ Stop at table: {table}")
                            continue
                        
                        table_info = self.client.get_table_metadata(table)
                        if table_info:
                            self.tables[table] = table_info
                            for upstream_job in table_info.upstream_jobs:
                                self.edges.append((upstream_job, f"table:{table}", "produces"))
                                if upstream_job not in visited_jobs:
                                    queue.append((upstream_job, depth + 1))
        
        print(f"\n[OK] Graph built: {len(self.jobs)} jobs, {len(self.tables)} tables, {len(self.edges)} edges")
    
    def generate_mermaid(self) -> str:
        """Generate Mermaid flowchart"""
        lines = ["flowchart TD"]
        
        # Add jobs as rectangles
        for job_id, job in self.jobs.items():
            label = f"{job.name or job_id}\\n[{job.status or 'UNKNOWN'}]"
            lines.append(f"    {self._safe_id(job_id)}[\"{label}\"]")
        
        # Add tables as cylinders
        for table_name, table in self.tables.items():
            label = f"📊 {table_name}\\n({table.source_type or 'Hive'})"
            lines.append(f"    {self._safe_id(f'table:{table_name}')}[(\"{label}\")]")
        
        # Add edges
        for from_node, to_node, edge_type in self.edges:
            from_id = self._safe_id(from_node)
            to_id = self._safe_id(to_node)
            
            if edge_type == "job_dependency":
                lines.append(f"    {from_id} -->|depends on| {to_id}")
            elif edge_type == "produces":
                if to_node.startswith("table:"):
                    lines.append(f"    {from_id} -->|produces| {to_id}")
                else:
                    lines.append(f"    {from_id} -->|from table| {to_id}")
        
        return "\n".join(lines)
    
    def _safe_id(self, node_id: str) -> str:
        """Convert node ID to safe Mermaid ID"""
        return node_id.replace("-", "_").replace(".", "_").replace(":", "_")


def main():
    parser = argparse.ArgumentParser(description="Analyze job dependencies and generate flowchart")
    parser.add_argument("--job-ids", required=True, help="Comma-separated job IDs")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum dependency depth")
    parser.add_argument("--stop-at-tables", help="Comma-separated table names to stop at")
    parser.add_argument("--downstream", action="store_true", help="Trace downstream dependencies")
    parser.add_argument("--zeus-url", default="http://zeus-osg-mcp-function.faas.ctripcorp.com/mcp")
    parser.add_argument("--metadata-url", default="http://metadata-osg-stream-function.faas.ctripcorp.com/mcp")
    parser.add_argument("--token", default="ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38")
    parser.add_argument("--output", help="Output file for Mermaid code")
    
    args = parser.parse_args()
    
    job_ids = [j.strip() for j in args.job_ids.split(",")]
    stop_tables = [t.strip() for t in args.stop_at_tables.split(",")] if args.stop_at_tables else None
    
    # Initialize MCP client
    client = MCPClient(args.zeus_url, args.metadata_url, args.token)
    
    # List available tools (for debugging)
    print("[INFO] Discovering Zeus MCP tools...")
    zeus_tools = client.list_tools(args.zeus_url)
    if zeus_tools:
        print(f"[OK] Zeus MCP tools: {zeus_tools}")
    
    print("[INFO] Discovering Metadata MCP tools...")
    metadata_tools = client.list_tools(args.metadata_url)
    if metadata_tools:
        print(f"[OK] Metadata MCP tools: {metadata_tools}")
    
    # Build dependency graph
    graph = DependencyGraph(client)
    graph.build_graph(job_ids, args.max_depth, stop_tables, args.downstream)
    
    # Generate Mermaid
    mermaid = graph.generate_mermaid()
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(mermaid)
        print(f"\n[OK] Mermaid flowchart saved to {args.output}")
    else:
        print("\n" + "="*60)
        print("Mermaid Flowchart:")
        print("="*60)
        print(mermaid)
    
    return mermaid


if __name__ == "__main__":
    main()
