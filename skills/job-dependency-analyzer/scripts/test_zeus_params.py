#!/usr/bin/env python3
"""
Test Zeus MCP - Try different parameter formats
"""

import requests
import json


def call_zeus_tool(tool_name: str, args: dict, token: str):
    """Call a Zeus MCP tool"""
    url = "http://zeus-osg-mcp-function.faas.ctripcorp.com/mcp"
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-bbzai-mcp-token": token
    })
    
    # Initialize
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        }
    }, timeout=30)
    
    session_id = resp.headers.get('mcp-session-id')
    session.headers['mcp-session-id'] = session_id
    
    # Call tool
    print(f"\nTool: {tool_name}, Args: {args}")
    
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }, timeout=60, stream=True)
    
    for line in resp.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith("data:"):
                try:
                    data = json.loads(line_str[5:].strip())
                    if "result" in data:
                        return data
                    elif "error" in data:
                        print(f"  Error: {data['error']}")
                except:
                    pass
    
    return None


if __name__ == "__main__":
    TOKEN = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    
    job_id = "965422"
    
    # Try different parameter formats
    param_variants = [
        {"job_id": job_id},
        {"id": job_id},
        {"jobId": job_id},
        {"job_id": int(job_id)},
        {"id": int(job_id)},
        {"jobId": int(job_id)},
        {"params": {"job_id": job_id}},
        {"params": {"id": job_id}},
        {"query": {"job_id": job_id}},
        {"filters": {"job_id": job_id}},
        {"job_id": job_id, "include_deps": True},
        {"job_id": job_id, "include_outputs": True},
        {"job_id": job_id, "include_downstream": True},
    ]
    
    tool_name = "get_job_info"
    
    print(f"Testing tool: {tool_name}")
    print(f"{'='*60}")
    
    for i, args in enumerate(param_variants):
        print(f"\n[{i+1}] Testing: {args}")
        result = call_zeus_tool(tool_name, args, TOKEN)
        if result and "result" in result:
            print(f"\n✅ SUCCESS!")
            print(f"Result: {json.dumps(result['result'], indent=2, ensure_ascii=False)[:1500]}")
            break
    else:
        print("\n\n❌ No parameter variant worked.")
        print("\nTrying alternative tool names with simple params...")
        
        # Try simpler tool names
        for tool in ["get_job", "query_job", "read_job"]:
            print(f"\nTrying: {tool}")
            result = call_zeus_tool(tool, {"job_id": job_id}, TOKEN)
            if result and "result" in result:
                print(f"✅ {tool} worked!")
                break
