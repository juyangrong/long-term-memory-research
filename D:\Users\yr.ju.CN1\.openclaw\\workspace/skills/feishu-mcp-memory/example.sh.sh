#!/bin/bash
# Feishu MCP Memory - 使用示例脚本
# 用于演示如何通过 MCP 协议操作飞书文档

MCP_URL="https://mcp.larkenterprise.com/mcp/mcp_vfBUl9iS3Jzl_Hhamam3col99qUfBx4_pwz52lLsR1y9Uuwfuuoi9QfZbM2ycvk_0AT1CO6Y_v_I"

# 初始化 MCP 连接
init_mcp() {
  echo "初始化 MCP 连接..."
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "initialize",
      "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
          "name": "openclaw",
          "version": "1.0"
        }
      }
    }' | jq .
}

# 获取可用工具列表
list_tools() {
  echo "获取可用工具列表..."
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": 2,
      "method": "tools/list",
      "params": {}
    }' | jq .
}

# 创建记忆文档
create_memory_doc() {
  local title="$1"
  local content="$2"
  
  echo "创建文档：$title"
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 3,
      \"method\": \"tools/call\",
      \"params\": {
        \"name\": \"创建云文档\",
        \"arguments\": {
          \"title\": \"$title\",
          \"markdown\": \"$content\"
        }
      }
    }" | jq .
}

# 更新文档（追加内容）
append_to_doc() {
  local doc_id="$1"
  local content="$2"
  
  echo "追加内容到文档：$doc_id"
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 4,
      \"method\": \"tools/call\",
      \"params\": {
        \"name\": \"更新云文档\",
        \"arguments\": {
          \"doc_id\": \"$doc_id\",
            \"mode\": \"append\",
          \"markdownmarkdown\": \"$content\"
        }
      }
    }" | jq .
}

# 搜索用户（获取 open_id）
search_user() {
  local query="$1"
  
  echo "搜索用户：$query"
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    "query\": \"$query\"
        }
      }
    }" | jq .
}

# 添加评论
add_comment() {
  local file_token="$1"
  local text="$2"
  
  echo "添加评论到文档：$file_token"
  curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 6,
      \"method\": \"tools/call\",
      \"params\": {
        \"name\": \"添加全文评论\",
        \"arguments\": {
          \"file_token\": \"$file_token\",
          \"elements\": [
            {\"type\": \"text\", \"text\": \"$text\"
          ]
        }
      }
    }" | jq .
}

# 主函数
main() {
  echo "=== Feishu MCP Memory 示例脚本 ==="
  echo "MCP URL: $MCP_URL"
  echo ""
  
  # 初始化
  init_mcp
  
  # 列出工具
  list_tools
  
  # 示例：创建测试文档
  # create_memory_doc "测试记忆文档" "# 测试内容\n\n这是一个测试文档。"
}

# 执行主函数
main "$@"
