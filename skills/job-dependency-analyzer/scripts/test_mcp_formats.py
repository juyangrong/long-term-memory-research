#!/usr/bin/env python3
"""
Test different MCP request formats
"""

import requests
import json


def test_mcp_formats():
    """Try different MCP request formats"""
    url = "http://zeus-osg-mcp-function.faas.ctripcorp.com/mcp"
    token = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    job_id = "965422"
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-bbzai-mcp-token": token
    })
    
    # Initialize first
    print("[1] Initialize...")
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        }
    })
    
    session_id = resp.headers.get('mcp-session-id')
    print(f"Session ID: {session_id}")
    session.headers['mcp-session-id'] = session_id
    
    # Try different formats for tools/call
    formats = [
        # Standard format
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "arguments": {"job_id": job_id}
            }
        },
        # Alternative: arguments at top level of params
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "job_id": job_id
            }
        },
        # Alternative: _params key
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "_arguments": {"job_id": job_id}
            }
        },
        # Alternative: no arguments wrapper
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "job_id": job_id
            }
        },
        # Alternative: data key
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "data": {"job_id": job_id}
            }
        },
        # Alternative: input key
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_job_info",
                "input": {"job_id": job_id}
            }
        },
        # Try with sessionId in params
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "sessionId": session_id,
                "name": "get_job_info",
                "arguments": {"job_id": job_id}
            }
        },
    ]
    
    print("\n[2] Testing different request formats...")
    for i, payload in enumerate(formats):
        print(f"\nFormat {i+1}: {json.dumps(payload, indent=2)[:200]}...")
        
        resp = session.post(url, json=payload, timeout=30, stream=True)
        
        for line in resp.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith("data:"):
                    try:
                        data = json.loads(line_str[5:].strip())
                        if "result" in data:
                            print(f"✅ SUCCESS with format {i+1}!")
                            print(f"Result: {json.dumps(data['result'], indent=2)[:500]}")
                            return True
                        elif "error" in data:
                            err = data['error']
                            print(f"  Error {err.get('code')}: {err.get('message')}")
                            if err.get('data'):
                                print(f"  Details: {err['data']}")
                    except Exception as e:
                        print(f"  Parse error: {e}")
    
    return False


if __name__ == "__main__":
    success = test_mcp_formats()
    if not success:
        print("\n\n❌ All formats failed.")
        print("\nPossible issues:")
        print("1. Tool 'get_job_info' doesn't exist")
        print("2. MCP server requires different authentication")
        print("3. Need to use a different method entirely")
