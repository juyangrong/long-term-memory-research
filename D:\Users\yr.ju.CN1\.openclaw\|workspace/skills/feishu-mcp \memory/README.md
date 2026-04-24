# # Feishu MCP Memory Skill

## 功能说明

使用飞书个人 MCP 权限进行文档操作，适用于：
- ✅ 创建飞书云文档
- ✅ 更新文档内容（追加/覆盖/替换）
- ✅ 添加文档评论（支持文本、@用户、超链接）
- ✅ 读取文档内容
- ✅ 作为 AI 长期记忆存储

## 配置

MCP 服务器 URL 已配置在 `config.json` 中：
```json
{
  "mcp": {
    "feishu_personal": {
      "url": "https://mcp.larkenterprise.com/mcp/mcp_vfBUl9iS3Jzl_Hhamd3col99qUfBx4_pwz52lLsR1y9Uuwfuuoi9QfZbM2ycvk_0AT1CO6Y_v_I"
    }
  }
}
```

## 使用方法

### 1. 创建记忆文档

```bash
# 调用 MCP 工具创建文档
curl -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "创建云文档",
      "arguments": {
        "title": "长期记忆 -2026-04-23",
        "markdown": "# 记忆内容\n\n..."
      }
    }
  }'
```

### 2. 更新文档

```bash
# 追加内容
curl -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "更新云文档",
      "arguments": {
        "doc_id": "文档 ID",
        "mode": "append",
        "markdown": "\n\n## 新增内容"
      }
    }
  }'
```

### 3. 添加评论（@用户）

```bash
# 先搜索用户
curl -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "search-user",
      "arguments": {"query": "用户姓名"}
    }
  }'

# 添加评论
curl -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "添加全文评论",
      "arguments": {
        "file_token": "文档 token",
        "elements": [
          {"type": "text", "text": "评论内容"},
          {"type": "mention", "open_id": "ou_xxx"}
        ]
      }
    }
  }'
```

## 约束条件

### ✅ 支持
- 纯文本
- @用户（需先调用 search-user 获取 open_id）
- 超链接

### ❌ 不支持
- 图片
- 附件/文件
- 表情符号
- 富文本格式（除基础 Markdown）

## 长期记忆模板

```markdown
# 长期记忆 - YYYY-MM-DD

## 📋 今日重点
- [关键决策]
- [重要信息]

## 🔧 技术笔记
- [新学到的技术]
- [问题解决记录]

## 📝 对话摘要
- [重要对话内容]

## ✅ 待办事项
- [需要跟进的任务]
```

## 注意事项

1. **Token 更新**: MCP token 会定期替换，请关注飞书通知
2. **用户搜索**: 禁止推测 open_id，必须通过 search-user 获取
3. **权限**: 使用个人 MCP 权限，无需应用权限配置

---

**版本**: 1.0.0  
**维护者**: AI Assistant  
**最后更新**: 2026-04-23
