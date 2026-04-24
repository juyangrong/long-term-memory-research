#!/usr/bin/env python3
"""
Test MCP resources and prompts (alternative to tools)
"""

import requests
import json


def test_mcp_resources():
    """Try MCP resources and prompts"""
    url = "http://zeus-osg-mcp-function.faas.ctripcorp.com/mcp"
    token = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-bbzai-mcp-token": token
    })
    
    # Initialize
    print("[1] Initialize...")
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {}
            },
            "clientInfo": {"name": "test", "version": "1.0.0"}
        }
    })
    
    content = resp.text
    print(f"Initialize response: {content[:800]}")
    
    session_id = resp.headers.get('mcp-session-id')
    session.headers['mcp-session-id'] = session_id
    
    # Try resources/list
    print("\n[2] Try resources/list...")
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "resources/list",
        "params": {}
    }, timeout=30, stream=True)
    
    for line in resp.iter_lines():
        if line:
            print(line.decode('utf-8'))
    
    # Try prompts/list
    print("\n[3] Try prompts/list...")
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 3,
        "method": "prompts/list",
        "params": {}
    }, timeout=30, stream=True)
    
    for line in resp.iter_lines():
        if line:
            print(line.decode('utf-8'))
    
    # Try reading a resource
    print("\n[4] Try resources/read with job info...")
    resp = session.post(url, json={
        "jsonrpc": "2.0",
        "id": 4,
        "method": "resources/read",
        "params": {
            "uri": f"zeus://job/965422"
        }
    }, timeout=30, stream=True)
    
    for line in resp.iter_lines():
        if line:
            print(line.decode('utf-8'))
    
    # Try with different URI patterns
    for uri_pattern in [
        f"zeus://jobs/965422",
        f"job://965422",
        f"zeus://job?id=965422",
        f"zeus://job/965422/info",
        f"zeus://job/965422/lineage",
    ]:
        print(f"\n[5] Try resources/read with URI: {uri_pattern}")
        resp = session.post(url, json={
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/read",
            "params": {"uri": uri_pattern}
        }, timeout=30, stream=True)
        
        for line in resp.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if "error" not in line_str.lower() or "result" in line_str.lower():
                    print(line_str)


if __name__ == "__main__":
    test_mcp_resources()
