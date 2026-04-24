#!/usr/bin/env python3
"""
Test direct HTTP API calls to Zeus (bypassing MCP protocol)
"""

import requests
import json


def test_direct_api():
    """Try direct HTTP API endpoints"""
    token = "ada_9989e898ece0b5f1fcd77d6756e4655ae34eb17001601e886d0e2078efca9c38"
    job_id = "965422"
    
    base_urls = [
        "http://zeus-osg-mcp-function.faas.ctripcorp.com",
        "http://zeus-osg-mcp-function.faas.ctripcorp.com/api",
        "http://zeus-osg-mcp-function.faas.ctripcorp.com/v1",
    ]
    
    endpoints = [
        "/job",
        "/job/info",
        "/jobs",
        f"/job/{job_id}",
        f"/jobs/{job_id}",
        f"/job/{job_id}/info",
        f"/job/{job_id}/dependencies",
        f"/job/{job_id}/downstream",
        f"/job/{job_id}/lineage",
    ]
    
    headers = {
        "x-bbzai-mcp-token": token,
        "Content-Type": "application/json"
    }
    
    print("Testing direct HTTP API endpoints")
    print("="*60)
    
    for base in base_urls:
        for endpoint in endpoints:
            url = f"{base}{endpoint}"
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                print(f"\n[{resp.status_code}] GET {url}")
                if resp.status_code == 200:
                    print(f"Response: {resp.text[:500]}")
                    return url
                elif resp.status_code not in [404, 405]:
                    print(f"Response: {resp.text[:200]}")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
    
    # Try POST
    print("\n\nTrying POST requests...")
    for base in base_urls:
        for endpoint in ["/job/query", "/job/search", "/job/get"]:
            url = f"{base}{endpoint}"
            try:
                resp = requests.post(url, headers=headers, json={"job_id": job_id}, timeout=10)
                print(f"\n[{resp.status_code}] POST {url}")
                if resp.status_code == 200:
                    print(f"Response: {resp.text[:500]}")
                    return url
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
    
    return None


if __name__ == "__main__":
    result = test_direct_api()
    if result:
        print(f"\n\n✅ Found working endpoint: {result}")
    else:
        print("\n\n❌ No working endpoint found.")
        print("\nNext steps:")
        print("1. Check Zeus MCP documentation for correct tool names")
        print("2. Verify token is correct and has proper permissions")
        print("3. Check if there's a different API endpoint")
