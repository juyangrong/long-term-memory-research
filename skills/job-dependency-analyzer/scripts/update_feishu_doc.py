#!/usr/bin/env python3
"""
Feishu Doc Updater - Updates Feishu document with job dependency flowchart

Usage:
    python update_feishu_doc.py --doc-token <doc_token> --mermaid-code "<mermaid>" --job-ids <job_ids>
"""

import argparse
import json
import requests
import sys
from typing import Optional


class FeishuDocUpdater:
    """Update Feishu document with job dependency analysis"""
    
    def __init__(self, doc_token: Optional[str] = None, folder_token: Optional[str] = None):
        self.doc_token = doc_token
        self.folder_token = folder_token
        self.base_url = "https://open.feishu.cn/open-apis/docx/v1"
        self.token = self._get_feishu_token()
    
    def _get_feishu_token(self) -> str:
        """Get Feishu API token from environment or config"""
        import os
        token = os.environ.get("FEISHU_APP_TOKEN")
        if not token:
            # Try to read from config file
            try:
                config_path = os.path.expanduser("~/.openclaw/extensions/feishu/config.json")
                with open(config_path) as f:
                    config = json.load(f)
                    token = config.get("app_token", "")
            except:
                pass
        
        if not token:
            print("[WARN] FEISHU_APP_TOKEN not set. Will use feishu-doc tool instead.")
            return ""
        
        return token
    
    def create_or_get_doc(self, title: str) -> str:
        """Create new document or return existing token"""
        if self.doc_token:
            return self.doc_token
        
        if not self.token:
            print(f"[INFO] Would create document: {title}")
            return ""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {"title": title}
            if self.folder_token:
                payload["folder_token"] = self.folder_token
            
            response = requests.post(
                f"{self.base_url}/documents",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.doc_token = result["data"]["document"]["doc_token"]
                print(f"[OK] Created document: {title} (token: {self.doc_token})")
                return self.doc_token
            else:
                print(f"[ERROR] Failed to create document: {response.text}")
                return ""
        except Exception as e:
            print(f"[ERROR] Exception creating document: {e}")
            return ""
    
    def update_content(self, content: str) -> bool:
        """Update document content using feishu-doc tool"""
        if not self.doc_token:
            print("[ERROR] No document token available")
            return False
        
        # Use feishu-doc tool via OpenClaw
        # This will be called by the main skill
        print(f"[INFO] Document token: {self.doc_token}")
        print(f"[INFO] Content length: {len(content)} chars")
        return True
    
    def generate_markdown(self, mermaid_code: str, job_ids: list, jobs: dict, tables: dict) -> str:
        """Generate markdown content for Feishu doc"""
        md = f"""# Job Dependency Analysis Report

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Job IDs:** {', '.join(job_ids)}

---

## 📊 Dependency Flowchart

```mermaid
{mermaid_code}
```

---

## 🔍 Job Details

"""
        
        for job_id, job in jobs.items():
            md += f"""### {job.get('name', job_id)}
- **Job ID:** `{job_id}`
- **Status:** {job.get('status', 'UNKNOWN')}
- **Run ID:** {job.get('run_id', 'N/A')}
- **Dependencies:** {', '.join(job.get('dependencies', [])) or 'None'}
- **Output Tables:** {', '.join(job.get('outputs', [])) or 'None'}

"""
        
        if tables:
            md += """---

## 📁 Table Metadata

"""
            for table_name, table in tables.items():
                md += f"""### {table_name}
- **Type:** {table.get('source_type', 'Hive')}
- **Environment:** {table.get('environment', 'N/A')}
- **Upstream Jobs:** {', '.join(table.get('upstream_jobs', [])) or 'None'}

"""
        
        md += """---

## 🛠️ How to Use This Skill

```bash
# Analyze job dependencies
python analyze_job_dependency.py --job-ids <job_id1,job_id2> --max-depth 5

# Stop at specific tables
python analyze_job_dependency.py --job-ids <job_id> --stop-at-tables "ods.table,ads.table"

# Output to file
python analyze_job_dependency.py --job-ids <job_id> --output flowchart.mmd
```

**Parameters:**
- `--job-ids`: Comma-separated job IDs to analyze
- `--max-depth`: Maximum dependency depth (default: 5)
- `--stop-at-tables`: Stop traversal at specific tables
- `--output`: Save Mermaid code to file
"""
        
        return md


def main():
    parser = argparse.ArgumentParser(description="Update Feishu document with job dependency analysis")
    parser.add_argument("--doc-token", help="Existing Feishu document token")
    parser.add_argument("--folder-token", help="Folder token for new document")
    parser.add_argument("--title", default="Job Dependency Analysis", help="Document title")
    parser.add_argument("--mermaid-code", required=True, help="Mermaid flowchart code")
    parser.add_argument("--job-ids", required=True, help="Comma-separated job IDs")
    parser.add_argument("--jobs-json", help="JSON string of job details")
    parser.add_argument("--tables-json", help="JSON string of table details")
    parser.add_argument("--output-markdown", help="Save markdown to file")
    
    args = parser.parse_args()
    
    updater = FeishuDocUpdater(args.doc_token, args.folder_token)
    
    # Parse job and table details
    jobs = json.loads(args.jobs_json) if args.jobs_json else {}
    tables = json.loads(args.tables_json) if args.tables_json else {}
    job_ids = [j.strip() for j in args.job_ids.split(",")]
    
    # Generate markdown
    md_content = updater.generate_markdown(args.mermaid_code, job_ids, jobs, tables)
    
    if args.output_markdown:
        with open(args.output_markdown, "w") as f:
            f.write(md_content)
        print(f"[OK] Markdown saved to {args.output_markdown}")
    
    # Create or get document
    doc_token = updater.create_or_get_doc(args.title)
    
    if doc_token:
        print(f"\n[OK] Document ready: https://xxx.feishu.cn/docx/{doc_token}")
        print("[INFO] Use feishu-doc tool to write content:")
        print(f'  {{ "action": "write", "doc_token": "{doc_token}", "content": <markdown> }}')
    else:
        print("\n[INFO] To create document manually, use feishu-doc tool:")
        print('  { "action": "create_and_write", "title": "Job Dependency Analysis", "content": <markdown> }')
    
    return md_content


if __name__ == "__main__":
    main()
