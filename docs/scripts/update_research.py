#!/usr/bin/env python3
"""
长期记忆研究资料自动更新脚本

功能:
1. 全网搜索最新资料 (论文、开源项目、工业案例)
2. 比对现有内容，识别更新
3. 更新相关文档
4. 生成更新报告

使用方式:
    python update_research.py [--dry-run] [--force]

定时任务 (每两天):
    0 2 */2 * * /path/to/venv/bin/python /path/to/update_research.py
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

class ResearchUpdater:
    """研究资料更新器"""
    
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root)
        self.research_dir = self.root / "memory-research"
        self.state_file = self.research_dir / ".update_state.json"
        self.log_file = self.research_dir / ".update_log.md"
        
        # 更新配置
        self.config = {
            "update_interval_days": 2,
            "max_results_per_search": 10,
            "confidence_threshold": 0.7,
        }
        
        # 加载状态
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载更新状态"""
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "last_update": None,
            "update_count": 0,
            "papers_tracked": [],
            "projects_tracked": [],
            "last_changes": []
        }
    
    def _save_state(self):
        """保存更新状态"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def check_update_needed(self) -> bool:
        """检查是否需要更新"""
        if not self.state["last_update"]:
            return True
        
        last_update = datetime.fromisoformat(self.state["last_update"])
        days_since = (datetime.now() - last_update).days
        return days_since >= self.config["update_interval_days"]
    
    def search_new_papers(self) -> List[Dict]:
        """搜索新论文 (模拟，实际应调用 API)"""
        # 这里模拟搜索结果，实际应调用 arXiv API 或 Google Scholar
        # 示例：使用 web_search 工具
        
        search_queries = [
            "long-term memory LLM agent 2026",
            "AI memory systems arXiv 2026",
            "conversational memory retrieval 2026",
        ]
        
        new_papers = []
        # 实际实现应调用 web_search API
        # 这里返回空列表，表示需要手动更新
        
        return new_papers
    
    def search_project_updates(self) -> List[Dict]:
        """搜索项目更新"""
        projects = [
            {"name": "Mem0", "url": "https://github.com/mem0ai/mem0"},
            {"name": "Letta", "url": "https://github.com/cpacker/Letta"},
            {"name": "LangChain", "url": "https://github.com/langchain-ai/langchain"},
        ]
        
        updates = []
        # 实际实现应调用 GitHub API 检查 release
        
        return updates
    
    def update_academic_frontiers(self, new_papers: List[Dict]):
        """更新学术研究前沿文档"""
        doc_path = self.research_dir / "03-全网资料深度探索" / "01-学术研究前沿.md"
        
        if not doc_path.exists():
            print(f"文档不存在：{doc_path}")
            return
        
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 添加新论文
        if new_papers:
            # 找到插入位置 (在 "更新记录" 之前)
            insert_pos = content.rfind("## 更新记录")
            if insert_pos == -1:
                insert_pos = len(content)
            
            new_section = "\n### 新发现论文\n\n"
            for paper in new_papers:
                new_section += f"#### {paper.get('title', 'Unknown')}\n"
                new_section += f"- **机构**: {paper.get('institution', 'Unknown')}\n"
                new_section += f"- **日期**: {paper.get('date', 'Unknown')}\n"
                new_section += f"- **链接**: {paper.get('link', '#')}\n"
                new_section += f"- **摘要**: {paper.get('abstract', 'N/A')}\n\n"
            
            content = content[:insert_pos] + new_section + content[insert_pos:]
            
            # 更新下次更新日期
            next_update = datetime.now() + timedelta(days=2)
            content = re.sub(
                r'\*\*下次更新\*\*: \d{4}-\d{2}-\d{2}',
                f'**下次更新**: {next_update.strftime("%Y-%m-%d")}',
                content
            )
        
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"已更新：{doc_path}")
    
    def update_industry_cases(self, new_cases: List[Dict]):
        """更新工业界落地案例"""
        doc_path = self.research_dir / "03-全网资料深度探索" / "02-工业界落地案例.md"
        
        if not doc_path.exists():
            return
        
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 添加新案例
        if new_cases:
            insert_pos = content.rfind("---\n\n## 更新记录")
            if insert_pos == -1:
                insert_pos = len(content)
            
            new_section = "\n## 新发现案例\n\n"
            for case in new_cases:
                new_section += f"### {case.get('company', 'Unknown')}\n\n"
                new_section += f"**行业**: {case.get('industry', 'Unknown')}\n\n"
                new_section += f"**背景**: {case.get('background', 'N/A')}\n\n"
                new_section += f"**方案**: {case.get('solution', 'N/A')}\n\n"
                new_section += f"**效果**: {case.get('results', 'N/A')}\n\n"
            
            content = content[:insert_pos] + new_section + content[insert_pos:]
        
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def update_open_source_comparison(self, updates: List[Dict]):
        """更新开源项目对比"""
        doc_path = self.research_dir / "03-全网资料深度探索" / "03-开源项目对比.md"
        
        # 类似上面的逻辑...
        pass
    
    def generate_update_report(self, changes: Dict) -> str:
        """生成更新报告"""
        report = f"""# 研究资料更新报告

**更新日期**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**更新类型**: {"定期" if changes.get("scheduled") else "手动"}

## 更新摘要

- 新论文：{len(changes.get("papers", []))} 篇
- 新项目更新：{len(changes.get("projects", []))} 个
- 新案例：{len(changes.get("cases", []))} 个

## 详细变更

### 论文更新
"""
        for paper in changes.get("papers", []):
            report += f"- {paper.get('title', 'Unknown')}\n"
        
        report += "\n### 项目更新\n"
        for proj in changes.get("projects", []):
            report += f"- {proj.get('name', 'Unknown')}: {proj.get('change', 'N/A')}\n"
        
        report += "\n### 案例更新\n"
        for case in changes.get("cases", []):
            report += f"- {case.get('company', 'Unknown')}\n"
        
        report += f"\n---\n*下次自动更新：{(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')}*\n"
        
        return report
    
    def run(self, dry_run: bool = False, force: bool = False):
        """执行更新"""
        print(f"🔍 开始更新研究资料...")
        print(f"工作目录：{self.root}")
        print(f"干运行：{dry_run}")
        print(f"强制更新：{force}")
        
        # 检查是否需要更新
        if not force and not self.check_update_needed():
            last_update = self.state["last_update"]
            print(f"⏭️  距离上次更新不足 {self.config['update_interval_days']} 天")
            print(f"   上次更新：{last_update}")
            return
        
        changes = {
            "scheduled": not force,
            "papers": [],
            "projects": [],
            "cases": []
        }
        
        if not dry_run:
            # 搜索新论文
            print("\n📚 搜索新论文...")
            changes["papers"] = self.search_new_papers()
            print(f"   发现 {len(changes['papers'])} 篇新论文")
            
            # 搜索项目更新
            print("\n🔧 搜索项目更新...")
            changes["projects"] = self.search_project_updates()
            print(f"   发现 {len(changes['projects'])} 个项目更新")
            
            # 更新文档
            print("\n✏️  更新文档...")
            self.update_academic_frontiers(changes["papers"])
            self.update_industry_cases(changes["cases"])
            self.update_open_source_comparison(changes["projects"])
            
            # 更新状态
            self.state["last_update"] = datetime.now().isoformat()
            self.state["update_count"] += 1
            self.state["last_changes"] = changes
            
            # 保存状态
            self._save_state()
            
            # 生成报告
            report = self.generate_update_report(changes)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n{report}\n")
            
            print(f"\n✅ 更新完成!")
            print(f"   更新报告：{self.log_file}")
        else:
            print("\n🔍 干运行模式，不实际更新")
            changes["papers"] = self.search_new_papers()
            changes["projects"] = self.search_project_updates()
            report = self.generate_update_report(changes)
            print(f"\n{report}")


def setup_cron_job(script_path: str, venv_python: str):
    """设置 crontab 定时任务"""
    import subprocess
    
    # Crontab 配置：每两天凌晨 2 点运行
    cron_entry = f"0 2 */2 * * {venv_python} {script_path} >> /tmp/memory_research_update.log 2>&1\n"
    
    # 获取当前 crontab
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_cron = result.stdout
    except subprocess.CalledProcessError:
        current_cron = ""
    
    # 检查是否已存在
    if script_path in current_cron:
        print("⚠️  定时任务已存在")
        return
    
    # 添加新任务
    new_cron = current_cron + cron_entry
    
    # 写入 crontab
    process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=new_cron)
    
    print("✅ 定时任务已设置：每两天凌晨 2 点运行")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="长期记忆研究资料自动更新")
    parser.add_argument("--dry-run", action="store_true", help="干运行，不实际更新")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--setup-cron", action="store_true", help="设置定时任务")
    parser.add_argument("--workspace", type=str, default=str(Path(__file__).parent.parent),
                       help="工作空间根目录")
    parser.add_argument("--python", type=str, default=sys.executable,
                       help="Python 解释器路径")
    
    args = parser.parse_args()
    
    # 初始化更新器
    updater = ResearchUpdater(args.workspace)
    
    # 设置定时任务
    if args.setup_cron:
        script_path = os.path.abspath(__file__)
        setup_cron_job(script_path, args.python)
        return
    
    # 执行更新
    updater.run(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
