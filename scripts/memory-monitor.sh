#!/bin/bash
# 定时任务监控主脚本
# 每周一执行，生成周报并推送

set -e

SCRIPTS_DIR="/home/rskuser/.openclaw/workspace/scripts"
LOG_DIR="/home/rskuser/.openclaw/workspace/memory/task-logs"
REPORT_DIR="/home/rskuser/.openclaw/workspace/memory/reports"

echo "=========================================="
echo "定时任务周报 - 监控执行"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# 1. 确保日志目录存在
mkdir -p "$LOG_DIR"
mkdir -p "$REPORT_DIR"

# 2. 生成周报
echo "📊 步骤 1: 生成周报"
echo "----------------------------------------"
"$SCRIPTS_DIR/memory-weekly-report.sh"
REPORT_STATUS=$?

if [ $REPORT_STATUS -eq 0 ]; then
    "$SCRIPTS_DIR/log-task.sh" "weekly-report" "success" "周报生成成功"
else
    "$SCRIPTS_DIR/log-task.sh" "weekly-report" "failed" "周报生成失败"
    echo "❌ 周报生成失败，退出"
    exit 1
fi

echo ""

# 3. 获取最新报告
LATEST_REPORT=$(ls -t "$REPORT_DIR"/weekly-report-*.md 2>/dev/null | head -1)

if [ -z "$LATEST_REPORT" ]; then
    echo "❌ 未找到报告文件"
    exit 1
fi

echo "📊 步骤 2: 读取报告内容"
echo "----------------------------------------"
echo "报告文件：$LATEST_REPORT"
echo ""

# 4. 推送飞书消息（通过工具）
echo "📤 步骤 3: 准备推送"
echo "----------------------------------------"

# 提取报告的关键信息（前 50 行）
SUMMARY=$(head -50 "$LATEST_REPORT")

cat << EOF

========================================
📋 推送内容预览
========================================

$SUMMARY

========================================
推送目标：杨荣 (ou_b148c321fa9f39bda5a30abab40118d7)
推送方式：飞书私信
========================================

EOF

echo ""
echo "✅ 监控执行完成"
echo ""
echo "📝 下一步："
echo "   1. 查看完整报告：$LATEST_REPORT"
echo "   2. 手动推送或使用 feishu_im_user_message 工具发送"
echo ""
