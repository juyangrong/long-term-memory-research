#!/bin/bash
# 完整重新推送脚本

set -e

cd /home/rskuser/.openclaw/workspace/github-memory-research

echo "================================"
echo "  重新推送项目到 GitHub"
echo "================================"
echo ""

# 1. 检查本地文件
echo "📦 1. 检查本地文件..."
file_count=$(find . -type f ! -path './.git/*' | wc -l)
echo "   文件数：$file_count"

if [ "$file_count" -eq 0 ]; then
    echo "   ❌ 本地没有文件！"
    exit 1
fi
echo "   ✅ 本地文件存在"
echo ""

# 2. 检查 Git 状态
echo "📋 2. 检查 Git 状态..."
git status --short | head -10

echo ""
echo "   添加所有文件..."
git add -A

echo "   提交文件..."
git commit -m "Complete project: Long-term memory research" || echo "   没有新更改"

git branch -M main
echo "   ✅ 提交完成"
echo ""

# 3. 使用 gh CLI 推送
echo "🚀 3. 使用 gh CLI 推送..."
if command -v gh &> /dev/null; then
    echo "   使用 gh repo push..."
    gh repo push --force 2>&1 | tail -5
    
    if [ $? -eq 0 ]; then
        echo "   ✅ gh CLI 推送成功"
    else
        echo "   ⚠️  gh CLI 推送失败，尝试 git push"
    fi
else
    echo "   ⚠️  gh 未安装，使用 git push"
fi

# 4. 使用 git push
echo ""
echo "🚀 4. 使用 git push..."
git push --force origin main 2>&1 | tail -10

if [ $? -eq 0 ]; then
    echo "   ✅ git push 成功"
else
    echo "   ❌ git push 失败"
fi
echo ""

# 5. 验证推送
echo "🔍 5. 验证推送..."
sleep 3

content_count=$(gh api repos/juyangrong/long-term-memory-research/contents 2>/dev/null | jq 'length')

if [ "$content_count" -gt 0 ]; then
    echo "   ✅ 验证成功！GitHub 上有 $content_count 个文件/目录"
    echo ""
    echo "   GitHub 内容:"
    gh api repos/juyangrong/long-term-memory-research/contents 2>/dev/null | jq -r '.[] | "   - \(.type): \(.name)"' | head -15
else
    echo "   ❌ 验证失败：GitHub 上仍然是空的"
    echo ""
    echo "   可能原因:"
    echo "   1. 推送被 GitHub 拒绝"
    echo "   2. 分支名不匹配"
    echo "   3. 权限问题"
    echo ""
    echo "   请检查错误信息"
fi

echo ""
echo "================================"
echo "  推送完成"
echo "================================"
echo ""
echo "访问地址:"
echo "  https://github.com/juyangrong/long-term-memory-research"
echo ""
