#!/bin/bash
# 飞书周报推送脚本（富文本格式 - 简化版）
# 用法：./push-weekly-report.sh <report_file>

set -e

REPORT_FILE="$1"
FEISHU_RECEIVE_ID="${FEISHU_RECEIVE_ID:-ou_b148c321fa9f39bda5a30abab40118d7}"

if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ 报告文件不存在：$REPORT_FILE"
    exit 1
fi

echo "📤 准备推送周报..."
echo "报告文件：$REPORT_FILE"
echo "推送目标：$FEISHU_RECEIVE_ID"
echo ""

# 从报告中提取关键信息
WEEK_NUM=$(grep -oP '周报 - \K\d{4}-W\d{2}' "$REPORT_FILE" | head -1)
TOTAL_EXEC=$(grep '总执行次数' "$REPORT_FILE" | grep -oP '\d+' | head -1 || echo "0")
TOTAL_SUCCESS=$(grep '✅ 成功' "$REPORT_FILE" | grep -oP '\d+' | head -1 || echo "0")
TOTAL_FAILED=$(grep '❌ 失败' "$REPORT_FILE" | grep -oP '\d+' | head -1 || echo "0")

# 默认值
WEEK_NUM=${WEEK_NUM:-"N/A"}
TOTAL_EXEC=${TOTAL_EXEC:-0}
TOTAL_SUCCESS=${TOTAL_SUCCESS:-0}
TOTAL_FAILED=${TOTAL_FAILED:-0}

if [ "$TOTAL_EXEC" -gt 0 ] 2>/dev/null; then
    SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($TOTAL_SUCCESS/$TOTAL_EXEC)*100}")
else
    SUCCESS_RATE="N/A"
fi

# 构建飞书富文本消息内容
TEXT_CONTENT="📊 定时任务周报 - $WEEK_NUM

📅 报告周期：上周
━━━━━━━━━━━━━━━━
📊 执行摘要
• 总执行：$TOTAL_EXEC 次
• ✅ 成功：$TOTAL_SUCCESS 次
• ❌ 失败：$TOTAL_FAILED 次
• 📈 成功率：$SUCCESS_RATE%
━━━━━━━━━━━━━━━━

📋 任务执行:"

# 添加任务详情（从 JSONL 日志提取）
LOG_FILE="/home/rskuser/.openclaw/workspace/memory/task-logs/$(date -d 'last week' +%Y-W%W).jsonl"
if [ -f "$LOG_FILE" ]; then
    while IFS= read -r line; do
        task=$(echo "$line" | jq -r '.task')
        status=$(echo "$line" | jq -r '.status')
        
        case "$status" in
            success) icon="✅" ;;
            failed) icon="❌" ;;
            *) icon="⏭️" ;;
        esac
        
        TEXT_CONTENT="$TEXT_CONTENT
• $icon $task"
    done < "$LOG_FILE"
else
    TEXT_CONTENT="$TEXT_CONTENT
• 暂无执行记录（新系统）"
fi

TEXT_CONTENT="$TEXT_CONTENT

━━━━━━━━━━━━━━━━
📄 完整报告：memory/reports/weekly-report-$WEEK_NUM.md"

# 输出调用参数
cat << EOF

========================================
📋 飞书消息调用命令
========================================

feishu_im_user_message \\
  --action send \\
  --receive_id "$FEISHU_RECEIVE_ID" \\
  --receive_id_type open_id \\
  --msg_type post \\
  --content '{
    "post": {
        "zh_cn": {
            "title": "📊 定时任务周报",
            "content": [
                [
                    {"tag": "text", "text": "'"$TEXT_CONTENT"'"}
                ]
            ]
        }
    }
  }'

========================================

EOF

echo "✅ 消息已生成（富文本格式）"
echo ""
echo "💡 格式说明："
echo "   • 使用 post 消息类型（飞书富文本）"
echo "   • 表格→列表格式（飞书私信不支持表格）"
echo "   • 支持点击链接查看完整报告"
echo ""
echo "📝 下一步："
echo "   1. 复制上面的命令"
echo "   2. 在终端执行（会自动调用飞书 API）"
echo "   3. 或集成到 HEARTBEAT.md 自动执行"
