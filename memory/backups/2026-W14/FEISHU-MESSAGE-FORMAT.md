# 飞书消息格式说明

**问题**: Markdown 表格在飞书私信中格式错乱  
**解决方案**: 使用飞书富文本（post）消息类型

---

## 📊 格式对比

### ❌ Markdown 表格（不支持）
```markdown
| 任务 | 成功 | 失败 | 成功率 |
|------|------|------|--------|
| 备份 | 3    | 0    | 100%   |
```
**结果**: 飞书私信显示为纯文本，格式错乱

---

### ✅ 飞书富文本（post 消息）
```json
{
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "📊 定时任务周报",
                "content": [
                    [
                        {"tag": "text", "text": "📋 任务详情\n• ✅ 记忆备份：成功 3 次\n• ✅ 健康监控：成功 1 次"}
                    ]
                ]
            }
        }
    }
}
```
**结果**: 飞书原生支持，格式整齐

---

## 🎯 推荐格式

### 列表格式（替代表格）

```
📊 执行摘要
━━━━━━━━━━━━━━━━
• 总执行：5 次
• ✅ 成功：5 次
• ❌ 失败：0 次
• 📈 成功率：100%
━━━━━━━━━━━━━━━━

📋 任务详情
• ✅ 记忆备份：成功 1 次 (100%)
• ✅ 健康监控：成功 1 次 (100%)
• ⏭️  记忆维护：跳过 0 次
━━━━━━━━━━━━━━━━

📄 完整报告：memory/reports/weekly-report-2026-W12.md
```

**优点**:
- ✅ 飞书私信完美支持
- ✅ 清晰易读
- ✅ 支持 emoji 图标
- ✅ 支持链接

---

## 🛠️ 使用工具

### 自动生成推送命令
```bash
cd /home/rskuser/.openclaw/workspace
./scripts/push-weekly-report.sh memory/reports/weekly-report-2026-W12.md
```

**输出**: 完整的 `feishu_im_user_message` 调用命令

### 手动发送
```bash
feishu_im_user_message \
  --action send \
  --receive_id "ou_b148c321fa9f39bda5a30abab40118d7" \
  --receive_id_type open_id \
  --msg_type post \
  --content '{
    "post": {
        "zh_cn": {
            "title": "📊 定时任务周报",
            "content": [
                [
                    {"tag": "text", "text": "消息内容"}
                ]
            ]
        }
    }
  }'
```

---

## 📝 消息类型对比

| 类型 | 支持表格 | 支持链接 | 支持@用户 | 推荐场景 |
|------|----------|----------|-----------|----------|
| **text** | ❌ | ❌ | ❌ | 简单文本 |
| **post** | ⚠️ 列表 | ✅ | ✅ | **周报推送** |
| **interactive** | ✅ 卡片 | ✅ | ✅ | 复杂交互 |

**推荐**: 周报推送使用 `post` 类型，平衡格式和复杂度

---

## 🔗 参考资料

- [飞书消息类型](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- [富文本消息格式](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN)
- [卡片消息构建器](https://open.feishu.cn/tool/cardbuilder)

---

**最后更新**: 2026-03-28  
**维护者**: 贾维斯 🏠
