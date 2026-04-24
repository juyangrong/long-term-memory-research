#!/usr/bin/env python3
"""
Test Zeus MCP - Try list operations and other tool patterns
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
    
    content = ""
    for line in resp.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            content += line_str + "\n"
            if line_str.startswith("data:"):
                try:
                    data = json.loads(line_str[5:].strip())
                    if "result" in data:
                        return data
                    elif "error" in data:
                        print(f"  Error: {data['error']}")
                except:
                    pass
    
    # Print raw response for debugging
    if "Invalid request" in content:
        print(f"  Raw: {content[:500]}")
    
    return None


if __name__ == "__main__":
    TOKEN = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    
    job_id = "965422"
    
    # Try list/search operations
    tools_to_try = [
        # List operations
        ("list_jobs", {}),
        ("listJobs", {}),
        ("jobs_list", {}),
        ("get_jobs", {}),
        ("query_jobs", {}),
        ("search_jobs", {}),
        
        # With job ID
        ("list_jobs", {"job_id": job_id}),
        ("list_jobs", {"id": job_id}),
        ("search_jobs", {"job_id": job_id}),
        
        # Dependency specific
        ("get_dependencies", {"job_id": job_id}),
        ("getDownstreamJobs", {"job_id": job_id}),
        ("get_upstream", {"job_id": job_id}),
        ("get_downstream", {"job_id": job_id}),
        ("job_dependencies", {"job_id": job_id}),
        ("job_lineage", {"job_id": job_id}),
        
        # Run specific
        ("get_job_runs", {"job_id": job_id}),
        ("getJobRuns", {"job_id": job_id}),
        ("list_job_runs", {"job_id": job_id}),
        
        # Output specific  
        ("get_job_outputs", {"job_id": job_id}),
        ("getJobOutputs", {"job_id": job_id}),
        ("get_output_tables", {"job_id": job_id}),
    ]
    
    print(f"Testing various Zeus MCP tools")
    print(f"{'='*60}")
    
    for tool_name, args in tools_to_try:
        print(f"\n[{tools_to_try.index((tool_name, args))+1}] Testing: {tool_name}({args})")
        result = call_zeus_tool(tool_name, args, TOKEN)
        if result and "result" in result:
            print(f"\n✅ SUCCESS with {tool_name}!")
            print(f"Result: {json.dumps(result['result'], indent=2, ensure_ascii=False)[:1500]}")
            break
    else:
        print("\n\n❌ None of the tools worked.")
        print("\nPossible issues:")
        print("1. Tool names are different from expected")
        print("2. MCP server requires specific authentication")
        print("3. Job ID format is incorrect")
        print("\nRecommendation: Check Zeus MCP documentation or API spec")
