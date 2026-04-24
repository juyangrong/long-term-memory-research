#!/usr/bin/env python3
"""
Job Dependency Analyzer - Main Entry Point

Analyzes job dependencies from Zeus MCP and Metadata MCP,
generates flowchart, and updates Feishu document.

Usage:
    python main.py --job-ids <job_id1,job_id2> --feishu-action create [--doc-token <token>]
"""

import argparse
import json
import subprocess
import sys
import os
from pathlib import Path


def run_script(script_name: str, args: list) -> tuple:
    """Run a script and return output"""
    script_path = Path(__file__).parent / "scripts" / script_name
    cmd = [sys.executable, str(script_path)] + args
    
    print(f"\n[INFO] Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="Job Dependency Analyzer")
    parser.add_argument("--job-ids", required=True, help="Comma-separated job IDs to analyze")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum dependency depth")
    parser.add_argument("--stop-at-tables", help="Comma-separated table names to stop at")
    parser.add_argument("--downstream", action="store_true", help="Trace downstream dependencies")
    parser.add_argument("--feishu-action", choices=["create", "update", "none"], default="create",
                       help="Feishu document action")
    parser.add_argument("--doc-token", help="Existing Feishu document token")
    parser.add_argument("--folder-token", help="Folder token for new document")
    parser.add_argument("--title", default="Job Dependency Analysis", help="Document title")
    parser.add_argument("--output-dir", help="Output directory for intermediate files")
    
    args = parser.parse_args()
    
    # Ensure output directory
    output_dir = args.output_dir or "/tmp/job-dependency"
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Analyze job dependencies
    print("="*60)
    print("Step 1: Analyzing Job Dependencies")
    print("="*60)
    
    analyze_args = [
        "--job-ids", args.job_ids,
        "--max-depth", str(args.max_depth),
    ]
    
    if args.stop_at_tables:
        analyze_args.extend(["--stop-at-tables", args.stop_at_tables])
    
    if args.downstream:
        analyze_args.append("--downstream")
    
    mermaid_file = os.path.join(output_dir, "flowchart.mmd")
    analyze_args.extend(["--output", mermaid_file])
    
    returncode, stdout, stderr = run_script("analyze_job_dependency.py", analyze_args)
    
    if returncode != 0:
        print(f"[ERROR] Analysis failed: {stderr}")
        return 1
    
    # Read Mermaid code
    with open(mermaid_file) as f:
        mermaid_code = f.read()
    
    # Step 2: Update Feishu document
    if args.feishu_action != "none":
        print("\n" + "="*60)
        print("Step 2: Updating Feishu Document")
        print("="*60)
        
        feishu_args = [
            "--mermaid-code", mermaid_code,
            "--job-ids", args.job_ids,
            "--title", args.title,
        ]
        
        if args.doc_token:
            feishu_args.extend(["--doc-token", args.doc_token])
        
        if args.folder_token:
            feishu_args.extend(["--folder-token", args.folder_token])
        
        md_file = os.path.join(output_dir, "report.md")
        feishu_args.extend(["--output-markdown", md_file])
        
        returncode, stdout, stderr = run_script("update_feishu_doc.py", feishu_args)
        
        if returncode != 0:
            print(f"[ERROR] Feishu update failed: {stderr}")
            return 1
        
        # Read markdown for feishu-doc tool
        with open(md_file) as f:
            markdown_content = f.read()
        
        print("\n" + "="*60)
        print("Step 3: Write to Feishu Document")
        print("="*60)
        print("\nUse the feishu-doc tool to write the content:")
        print(f"\nAction: {'write' if args.doc_token else 'create_and_write'}")
        
        if args.doc_token:
            print(f"doc_token: {args.doc_token}")
        else:
            print(f"title: {args.title}")
        
        print(f"content: (markdown content, {len(markdown_content)} chars)")
        print("\nOr use OpenClaw sessions_send to call feishu-doc tool automatically.")
    
    print("\n" + "="*60)
    print("✅ Job Dependency Analysis Complete!")
    print("="*60)
    print(f"\nOutput files:")
    print(f"  - Mermaid flowchart: {mermaid_file}")
    if args.feishu_action != "none":
        print(f"  - Markdown report: {md_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
