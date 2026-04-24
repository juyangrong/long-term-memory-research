#!/usr/bin/env python3
"""
MCP Tool Discovery - Lists available tools from MCP servers
"""

import requests
import json


def discover_tools(url: str, token: str, name: str):
    """Discover tools from MCP server using streamable HTTP"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-bbzai-mcp-token": token
    })
    
    print(f"\n{'='*60}")
    print(f"Discovering {name}...")
    print(f"{'='*60}")
    
    # Step 1: Initialize and get session ID
    print("\n[1] Initializing session...")
    session_id = None
    try:
        response = session.post(url, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "tool-discovery", "version": "1.0.0"}
            }
        }, timeout=30)
        
        content = response.text
        print(f"Response headers: {dict(response.headers)}")
        print(f"Raw response: {content[:500]}...")
        
        # Check for session ID in headers (MCP uses 'mcp-session-id')
        session_id = response.headers.get('mcp-session-id') or response.headers.get('x-session-id') or response.headers.get('session-id')
        
        if "data:" in content:
            data_part = content.split("data:")[1].strip()
            result = json.loads(data_part)
            print(f"[OK] Server: {result.get('result', {}).get('serverInfo', {})}")
            
            # Try to get session ID from result
            if not session_id:
                session_id = result.get('result', {}).get('sessionId')
        
        print(f"[OK] Session ID: {session_id}")
    except Exception as e:
        print(f"[ERROR] Initialize failed: {e}")
        return
    
    # Step 2: List tools with session ID
    print("\n[2] Listing tools...")
    if session_id:
        print(f"Using session ID: {session_id}")
        # Try both header and body
        session.headers['mcp-session-id'] = session_id
    
    try:
        # tools/list doesn't need params, but session ID must be in header
        response = session.post(url, json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }, timeout=30)
        
        content = response.text
        print(f"Response headers: {dict(response.headers)}")
        print(f"Raw response: {content[:1000]}...")
        
        # Parse SSE
        if "data:" in content:
            for line in content.split("\n"):
                if line.startswith("data:"):
                    data_part = line[5:].strip()
                    if data_part:
                        result = json.loads(data_part)
                        if "result" in result and "tools" in result["result"]:
                            tools = result["result"]["tools"]
                            print(f"\n[OK] Found {len(tools)} tools:")
                            for tool in tools:
                                print(f"  - {tool.get('name', 'unknown')}")
                                if 'description' in tool:
                                    print(f"    Description: {tool['description'][:100]}...")
                                if 'inputSchema' in tool:
                                    print(f"    Input schema: {json.dumps(tool['inputSchema'], indent=4)[:200]}...")
                        else:
                            print(f"[WARN] Unexpected response: {result}")
    except Exception as e:
        print(f"[ERROR] List tools failed: {e}")


if __name__ == "__main__":
    TOKEN = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    
    discover_tools(
        "http://zeus-osg-mcp-function.faas.ctripcorp.com/mcp",
        TOKEN,
        "Zeus MCP"
    )
    
    discover_tools(
        "http://metadata-osg-stream-function.faas.ctripcorp.com/mcp",
        TOKEN,
        "Metadata MCP"
    )
