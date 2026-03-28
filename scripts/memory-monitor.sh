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

# 4. 推送飞书消息（使用富文本格式）
echo "📤 步骤 3: 生成推送消息"
echo "----------------------------------------"

# 使用新的推送脚本（生成飞书富文本格式）
"$SCRIPTS_DIR/push-weekly-report.sh" "$LATEST_REPORT"

echo ""
echo "✅ 监控执行完成"
echo ""
echo "📝 下一步："
echo "   1. 复制上面的 content JSON"
echo "   2. 使用 feishu_im_user_message 工具发送"
echo "   3. 或查看完整报告：$LATEST_REPORT"
echo ""
