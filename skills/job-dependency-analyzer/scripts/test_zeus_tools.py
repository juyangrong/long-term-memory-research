#!/usr/bin/env python3
"""
Test Zeus MCP - Try common tool names to get job info
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
    print(f"\n[1] Initializing...")
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
    print(f"Session ID: {session_id}")
    session.headers['mcp-session-id'] = session_id
    
    # Call tool
    print(f"\n[2] Calling tool: {tool_name}")
    print(f"Args: {args}")
    
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }, timeout=60, stream=True)
    
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}")
    print(f"\nResponse:")
    
    for line in resp.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            print(line_str)
            if line_str.startswith("data:"):
                try:
                    data = json.loads(line_str[5:].strip())
                    if "result" in data:
                        print(f"\n[OK] Result: {json.dumps(data['result'], indent=2, ensure_ascii=False)}")
                        return data
                except:
                    pass
    
    return None


if __name__ == "__main__":
    TOKEN = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    
    # Try common tool names for getting job info
    tool_names = [
        "get_job",
        "get_job_info", 
        "get_job_detail",
        "query_job",
        "fetch_job",
        "zeus_get_job",
        "getJob",
        "getJobInfo",
        "job_get",
        "job_info",
        "read_job",
        "describe_job"
    ]
    
    job_id = "965422"
    
    for tool_name in tool_names:
        print(f"\n{'='*60}")
        print(f"Trying: {tool_name}")
        print(f"{'='*60}")
        
        try:
            result = call_zeus_tool(tool_name, {"job_id": job_id}, TOKEN)
            if result and "result" in result:
                print(f"\n✅ SUCCESS with tool: {tool_name}")
                print(f"Result: {json.dumps(result['result'], indent=2, ensure_ascii=False)[:1000]}")
                break
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print("\n\nDone testing.")
