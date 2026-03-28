#!/bin/bash
# 飞书消息推送脚本
# 用法：./send-feishu-message.sh <message_content>

set -e

# 配置项（从环境变量或配置文件读取）
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
FEISHU_RECEIVE_ID="${FEISHU_RECEIVE_ID:-ou_b148c321fa9f39bda5a30abab40118d7}"
FEISHU_RECEIVE_ID_TYPE="${FEISHU_RECEIVE_ID_TYPE:-open_id}"

# 消息内容（从 stdin 或参数读取）
if [ -n "$1" ]; then
    MESSAGE_CONTENT="$1"
else
    MESSAGE_CONTENT=$(cat)
fi

if [ -z "$MESSAGE_CONTENT" ]; then
    echo "错误：消息内容为空"
    echo "用法：$0 <message_content> 或 echo '消息' | $0"
    exit 1
fi

# 如果没有配置 webhook，使用 feishu_im_user_message 工具
if [ -z "$FEISHU_WEBHOOK_URL" ]; then
    echo "ℹ️  未配置 Webhook，使用 feishu_im_user_message 工具"
    echo ""
    echo "【定时任务周报】"
    echo ""
    echo "$MESSAGE_CONTENT"
    echo ""
    echo "---"
    echo "推送目标：$FEISHU_RECEIVE_ID"
    echo "推送方式：feishu_im_user_message 工具"
    exit 0
fi

# 使用 Webhook 推送
echo "📤 推送飞书消息..."

# 构建 JSON  payload
PAYLOAD=$(cat << EOF
{
    "msg_type": "text",
    "content": {
        "text": "【定时任务周报】\n\n$MESSAGE_CONTENT"
    }
}
EOF
)

# 发送请求
RESPONSE=$(curl -s -X POST "$FEISHU_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

echo "响应：$RESPONSE"

# 检查响应
if echo "$RESPONSE" | jq -e '.StatusCode == 0' > /dev/null 2>&1; then
    echo "✅ 消息推送成功"
    exit 0
else
    echo "❌ 消息推送失败"
    echo "错误详情：$RESPONSE"
    exit 1
fi
