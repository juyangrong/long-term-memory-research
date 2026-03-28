# 定时任务监控 - 快速参考

**创建时间**: 2026-03-28  
**维护者**: 贾维斯 🏠

---

## 🚀 快速命令

### 查看任务清单
```bash
cat /home/rskuser/.openclaw/workspace/memory/TASK-SCHEDULE.md
```

### 手动执行任务
```bash
# 记忆备份
cd /home/rskuser/.openclaw/workspace
./scripts/memory-backup.sh

# 记忆压缩（预览）
DRY_RUN=true ./scripts/memory-compact.sh

# 生成周报
./scripts/memory-monitor.sh

# 推送周报（飞书富文本格式）
./scripts/push-weekly-report.sh memory/reports/weekly-report-2026-W12.md
```

### 查看日志
```bash
# 本周任务日志
cat /home/rskuser/.openclaw/workspace/memory/task-logs/$(date +%Y-W%W).jsonl

# 今日日志
cat /home/rskuser/.openclaw/workspace/memory/task-logs/$(date +%Y-%m-%d).md

# 最新周报
ls -t /home/rskuser/.openclaw/workspace/memory/reports/weekly-report-*.md | head -1 | xargs cat
```

### 手动记录任务
```bash
./scripts/log-task.sh <任务名> <状态> [备注]

# 示例
./scripts/log-task.sh "memory-backup" "success" "备份 5 个文件"
./scripts/log-task.sh "health-check" "failed" "Ollama 服务未响应"
```

---

## 📅 任务时间表

| 时间 | 任务 | 推送 |
|------|------|------|
| **周日 23:00** | 记忆备份 | ❌ |
| **周一 09:00** | 健康监控 | ❌ |
| **周一 09:30** | 周报生成 | ✅ 飞书私信 |
| **每月 1 号 10:00** | 记忆维护 | ❌ |

---

## 📊 日志位置

| 类型 | 路径 |
|------|------|
| 任务日志 | `memory/task-logs/YYYY-Www.jsonl` |
| 每日汇总 | `memory/task-logs/YYYY-MM-DD.md` |
| 周报报告 | `memory/reports/weekly-report-YYYY-Www.md` |
| 备份文件 | `memory/backups/YYYY-Www/` |

---

## 🔧 故障排查

### 任务未执行
```bash
# 检查 Heartbeat 配置
cat /home/rskuser/.openclaw/workspace/HEARTBEAT.md

# 手动执行任务
./scripts/memory-backup.sh
```

### 日志未记录
```bash
# 检查日志目录
ls -la /home/rskuser/.openclaw/workspace/memory/task-logs/

# 测试日志记录
./scripts/log-task.sh "test" "success" "测试"
```

### 周报未推送
```bash
# 生成周报
./scripts/memory-monitor.sh

# 手动发送飞书消息
# 使用 feishu_im_user_message 工具
```

---

## 📞 联系

如有问题，请查看：
- 完整文档：`memory/TASK-SCHEDULE.md`
- 压缩指南：`memory/MEMORY-COMPACT-GUIDE.md`
- 心跳配置：`HEARTBEAT.md`

---

*快速参考卡片 - 打印或收藏*
