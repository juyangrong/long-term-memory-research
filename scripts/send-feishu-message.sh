#!/bin/bash
# 飞书消息推送脚本
# 用法：./send-feishu-message.sh <message_content> [--format text|post|interactive]

set -e

# 配置项
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
FEISHU_RECEIVE_ID="${FEISHU_RECEIVE_ID:-ou_b148c321fa9f39bda5a30abab40118d7}"
FEISHU_RECEIVE_ID_TYPE="${FEISHU_RECEIVE_ID_TYPE:-open_id}"
MSG_FORMAT="${MSG_FORMAT:-post}"  # text, post, interactive

# 消息内容（从 stdin 或参数读取）
if [ -n "$1" ] && [ "$1" != "--format" ]; then
    MESSAGE_CONTENT="$1"
    shift
fi

# 解析 --format 参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            MSG_FORMAT="$2"
            shift 2
            ;;
        *)
            MESSAGE_CONTENT="$1"
            shift
            ;;
    esac
done

if [ -z "$MESSAGE_CONTENT" ]; then
    MESSAGE_CONTENT=$(cat)
fi

if [ -z "$MESSAGE_CONTENT" ]; then
    echo "错误：消息内容为空"
    echo "用法：$0 <message_content> [--format text|post|interactive]"
    exit 1
fi

echo "📤 推送飞书消息..."
echo "格式：$MSG_FORMAT"
echo "目标：$FEISHU_RECEIVE_ID"
echo ""

# 如果没有配置 webhook，使用 feishu_im_user_message 工具
if [ -z "$FEISHU_WEBHOOK_URL" ]; then
    echo "ℹ️  未配置 Webhook，生成 feishu_im_user_message 调用参数"
    echo ""
    
    case "$MSG_FORMAT" in
        post)
            # 飞书富文本格式
            echo "【推荐】使用 post 消息类型（富文本）"
            echo ""
            echo "msg_type: post"
            echo "content 示例:"
            cat << EOF
{
    "post": {
        "zh_cn": {
            "title": "【定时任务周报】",
            "content": [
                [
                    {"tag": "text", "text": "📊 执行摘要\n"},
                    {"tag": "text", "text": "总执行次数：X\n"},
                    {"tag": "text", "text": "成功率：XX%\n\n"},
                    {"tag": "text", "text": "📋 任务详情\n"},
                    {"tag": "text", "text": "✅ 记忆备份：成功 1 次\n"},
                    {"tag": "text", "text": "✅ 健康监控：成功 1 次\n"}
                ]
            ]
        }
    }
}
EOF
            ;;
        interactive)
            echo "【高级】使用 interactive 消息类型（卡片）"
            echo "需要构建卡片 JSON，参考：https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN"
            ;;
        *)
            echo "【基础】使用 text 消息类型"
            echo "content: {\"text\":\"【定时任务周报】\\n\\n$MESSAGE_CONTENT\"}"
            ;;
    esac
    
    echo ""
    echo "---"
    echo "提示：在 memory-monitor.sh 中调用 feishu_im_user_message 工具发送"
    exit 0
fi

# 使用 Webhook 推送
case "$MSG_FORMAT" in
    post)
        # 构建富文本 payload
        PAYLOAD=$(cat << EOF
{
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "【定时任务周报】",
                "content": [
                    [
                        {"tag": "text", "text": "$MESSAGE_CONTENT"}
                    ]
                ]
            }
        }
    }
}
EOF
)
        ;;
    interactive)
        # 构建卡片 payload（简化版）
        PAYLOAD=$(cat << EOF
{
    "msg_type": "interactive",
    "content": {
        "card_link": {
            "url": "https://example.com"
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "【定时任务周报】"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "$MESSAGE_CONTENT"
                }
            }
        ]
    }
}
EOF
)
        ;;
    *)
        PAYLOAD=$(cat << EOF
{
    "msg_type": "text",
    "content": {
        "text": "【定时任务周报】\n\n$MESSAGE_CONTENT"
    }
}
EOF
)
        ;;
esac

# 发送请求
RESPONSE=$(curl -s -X POST "$FEISHU_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

echo "响应：$RESPONSE"

if echo "$RESPONSE" | jq -e '.StatusCode == 0' > /dev/null 2>&1; then
    echo "✅ 消息推送成功"
    exit 0
else
    echo "❌ 消息推送失败"
    echo "错误详情：$RESPONSE"
    exit 1
fi
