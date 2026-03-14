#!/usr/bin/env python3
"""
长期记忆研究资料 - 自动更新和推送脚本

功能:
1. 检查并更新研究资料
2. 自动提交到 Git
3. 推送到 GitHub
4. 每两天自动执行
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE_ROOT = Path(__file__).parent.parent
RESEARCH_DIR = WORKSPACE_ROOT / "github-memory-research"
LOG_FILE = WORKSPACE_ROOT / "update_log.md"
UPDATE_INTERVAL_DAYS = 2

def run_command(cmd, cwd=None):
    """执行 shell 命令"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or WORKSPACE_ROOT,
            capture_output=True, 
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_git_status():
    """检查 Git 状态"""
    print("📋 检查 Git 状态...")
    success, output = run_command("git status --porcelain", cwd=RESEARCH_DIR)
    if not success:
        print("❌ Git 仓库未初始化")
        return False
    
    has_changes = bool(output.strip())
    print(f"   工作区{'有' if has_changes else '无'}更改")
    return True

def commit_and_push(message="Auto update research"):
    """提交并推送"""
    print("📝 提交更改...")
    
    # Add all files
    success, _ = run_command("git add -A", cwd=RESEARCH_DIR)
    if not success:
        print("❌ git add 失败")
        return False
    
    # Check if there are changes
    success, output = run_command("git diff --cached --porcelain", cwd=RESEARCH_DIR)
    if not output.strip():
        print("⏭️  没有更改，跳过提交")
        return True
    
    # Commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"{message}\n\nTimestamp: {timestamp}"
    success, _ = run_command(f'git commit -m "{commit_msg}"', cwd=RESEARCH_DIR)
    if not success:
        print("❌ git commit 失败")
        return False
    
    print("✅ 提交成功")
    
    # Push
    print("🚀 推送到 GitHub...")
    success, output = run_command("git push origin main", cwd=RESEARCH_DIR)
    if not success:
        print(f"❌ git push 失败：{output}")
        return False
    
    print("✅ 推送成功")
    return True

def update_log(message="Updated"):
    """更新日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"## {timestamp}\n\n- {message}\n\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def main():
    """主函数"""
    print("=" * 50)
    print("  长期记忆研究资料 - 自动更新")
    print("=" * 50)
    print()
    
    # 检查目录
    if not RESEARCH_DIR.exists():
        print(f"❌ 目录不存在：{RESEARCH_DIR}")
        sys.exit(1)
    
    # 检查 Git
    if not check_git_status():
        sys.exit(1)
    
    # 提交并推送
    if not commit_and_push():
        sys.exit(1)
    
    # 更新日志
    update_log("Auto update completed")
    
    print()
    print("=" * 50)
    print("✅ 更新完成")
    print("=" * 50)
    print()
    print(f"📝 日志：{LOG_FILE}")
    print(f"🌐 仓库：https://github.com/juyangrong/long-term-memory-research")

if __name__ == "__main__":
    main()
