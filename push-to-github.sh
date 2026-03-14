#!/bin/bash
# GitHub 推送脚本
# 使用方式：./push-to-github.sh

set -e

REPO_NAME="long-term-memory-research"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  推送到 GitHub${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查 Git 配置
echo -e "${YELLOW}📋 检查 Git 配置...${NC}"
git_user=$(git config user.name 2>/dev/null || echo "")
git_email=$(git config user.email 2>/dev/null || echo "")

if [ -z "$git_user" ] || [ -z "$git_email" ]; then
    echo -e "${RED}❌ 需要配置 Git 用户信息${NC}"
    echo ""
    echo "请运行以下命令:"
    echo "  git config --global user.name \"Your Name\""
    echo "  git config --global user.email \"your.email@example.com\""
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Git 用户：$git_user <$git_email>${NC}"
echo ""

# 检查远程仓库
echo -e "${YELLOW}🔗 检查远程仓库...${NC}"
remote_url=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$remote_url" ]; then
    echo -e "${RED}❌ 未配置远程仓库${NC}"
    echo ""
    echo "请按以下步骤操作:"
    echo ""
    echo "1. 在 GitHub 创建新仓库:"
    echo "   访问：https://github.com/new"
    echo "   仓库名：$REPO_NAME"
    echo "   描述：Comprehensive research on long-term memory for AI agents"
    echo "    visibility: Public"
    echo "   ⚠️  不要勾选 'Initialize this repository with a README'"
    echo ""
    echo "2. 创建完成后，将仓库 URL 填入下方:"
    echo ""
    read -p "GitHub 仓库 URL (如：https://github.com/yrju/$REPO_NAME.git): " repo_url
    
    if [ -z "$repo_url" ]; then
        echo -e "${RED}❌ 未输入仓库 URL${NC}"
        exit 1
    fi
    
    git remote add origin "$repo_url"
    remote_url="$repo_url"
fi

echo -e "${GREEN}✅ 远程仓库：$remote_url${NC}"
echo ""

# 推送
echo -e "${YELLOW}🚀 推送到 GitHub...${NC}"
echo ""

# 检查是否需要强制推送
if git rev-parse --verify origin/main &>/dev/null; then
    echo -e "${YELLOW}⚠️  远程已有 main 分支，是否强制推送？${NC}"
    read -p "强制推送会覆盖远程历史 (y/N): " force
    
    if [ "$force" = "y" ] || [ "$force" = "Y" ]; then
        git push -f origin main
    else
        git push origin main
    fi
else
    # 首次推送
    git push -u origin main
fi

echo ""
echo -e "${GREEN}✅ 推送成功!${NC}"
echo ""

# 提取仓库信息
repo_name=$(echo "$remote_url" | sed -n 's/.*github\.com[:/]\([^/]*\)\/\([^/]*\)\.git/\1\/\2/p')

echo -e "${BLUE}📊 项目信息:${NC}"
echo "  仓库：$repo_name"
echo "  分支：main"
echo ""
echo -e "${BLUE}🔗 访问地址:${NC}"
echo "  https://github.com/$repo_name"
echo ""
echo -e "${YELLOW}📝 下一步:${NC}"
echo "  1. 在 GitHub 查看项目"
echo "  2. 添加项目描述和话题标签"
echo "  3. 设置 GitHub Pages (可选)"
echo "  4. 配置 GitHub Actions (可选)"
echo ""
