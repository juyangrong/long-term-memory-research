# 定时任务清单与监控配置

**最后更新**: 2026-03-28  
**维护者**: 贾维斯 🏠

---

## 📋 定时任务总览

| # | 任务名称 | 频率 | 执行时间 | 脚本 | 状态 |
|---|----------|------|----------|------|------|
| 1 | 记忆健康监控 | 每周 | 周一 09:00 | HEARTBEAT.md | 🟢 已配置 |
| 2 | 记忆备份 | 每周 | 周日 23:00 | memory-backup.sh | 🟢 已配置 |
| 3 | 记忆维护 | 每月 | 1 号 10:00 | HEARTBEAT.md | 🟢 已配置 |
| 4 | 周报生成与推送 | 每周 | 周一 09:30 | memory-monitor.sh | 🟢 已配置 |

---

## 🔧 任务详情

### 1️⃣ 记忆健康监控

**执行频率**: 每周一 09:00  
**触发方式**: Heartbeat 会话  
**配置位置**: `HEARTBEAT.md`

**检查内容**:
```bash
# 1. OpenClaw 记忆状态
openclaw memory status 2>&1 | head -20

# 2. Ollama 服务状态
curl -s http://localhost:11434/api/tags | jq -r '.models[].name'

# 3. 记忆文件完整性
ls -lh /home/rskuser/.openclaw/workspace/memory/*.md | tail -5
```

**预期结果**:
- ✅ 无 "Local embeddings unavailable" 错误
- ✅ 返回 `nomic-embed-text:latest`
- ✅ 存在最近的记忆文件

**异常处理**:
- Ollama 服务未响应 → `systemctl restart ollama`
- 记忆状态报错 → 记录到 `memory/diagnostic-YYYY-MM-DD.md`
- 连续 2 周失败 → 通知用户

---

### 2️⃣ 记忆备份

**执行频率**: 每周日 23:00  
**触发方式**: Heartbeat 会话  
**脚本**: `scripts/memory-backup.sh`

**执行内容**:
```bash
cd /home/rskuser/.openclaw/workspace
./scripts/memory-backup.sh
```

**备份内容**:
- 所有 `memory/*.md` 文件
- 周备份目录：`memory/backups/YYYY-Www/`
- 备份元数据：`BACKUP_INFO.md`
- Git 自动提交

**保留策略**: 12 周（约 3 个月）

---

### 3️⃣ 记忆维护

**执行频率**: 每月 1 号 10:00  
**触发方式**: Heartbeat 会话  
**配置位置**: `HEARTBEAT.md`

**执行内容**:
```bash
# 1. 整理旧日志（预览模式）
DRY_RUN=true ./scripts/memory-compact.sh

# 2. 手动审查后执行实际清理
DRY_RUN=false ./scripts/memory-compact.sh
```

**维护内容**:
- 整理超过 7 天的日志到 MEMORY.md
- 清理超过 30 天的日志文件
- 验证备份完整性

---

### 4️⃣ 周报生成与推送

**执行频率**: 每周一 09:30  
**触发方式**: Heartbeat 会话  
**脚本**: `scripts/memory-monitor.sh`

**执行流程**:
```bash
# 1. 生成周报
./scripts/memory-weekly-report.sh

# 2. 记录执行状态
./scripts/log-task.sh "weekly-report" "success" "周报生成成功"

# 3. 推送飞书消息
# （通过 feishu_im_user_message 工具）
```

**推送内容**:
- 上周任务执行摘要
- 各任务成功率统计
- 失败任务告警
- 改进建议

**推送目标**: 杨荣 (ou_b148c321fa9f39bda5a30abab40118d7)

---

## 📊 监控日志

### 日志位置
| 类型 | 位置 | 格式 |
|------|------|------|
| 任务执行日志 | `memory/task-logs/YYYY-Www.jsonl` | JSONL |
| 每日汇总 | `memory/task-logs/YYYY-MM-DD.md` | Markdown |
| 周报报告 | `memory/reports/weekly-report-YYYY-Www.md` | Markdown |

### 日志格式
```json
{"timestamp":"2026-03-28 16:00:00","date":"2026-03-28","week":"2026-W12","task":"memory-backup","status":"success","message":"备份 5 个文件"}
```

### 状态说明
| 状态 | 说明 |
|------|------|
| `success` | 任务执行成功 |
| `failed` | 任务执行失败 |
| `skipped` | 任务被跳过（未到执行时间） |

---

## 🔔 告警机制

### 告警级别
| 级别 | 触发条件 | 响应 |
|------|----------|------|
| 🟢 正常 | 所有任务成功 | 周报汇总 |
| 🟡 警告 | 单个任务失败 | 周报中标记 |
| 🟠 关注 | 同一任务连续 2 次失败 | 单独通知 |
| 🔴 严重 | 所有任务失败 | 立即通知 + 诊断 |

### 告警方式
- **周报汇总**: 飞书私信（每周一 09:30）
- **单独通知**: 飞书私信（任务失败时）
- **立即通知**: 飞书私信 + 声音提醒（严重故障）

---

## 🛠️ 工具脚本

| 脚本 | 功能 | 用法 |
|------|------|------|
| `log-task.sh` | 记录任务执行日志 | `./log-task.sh <task> <status> [message]` |
| `memory-backup.sh` | 记忆备份 | `./memory-backup.sh` |
| `memory-compact.sh` | 记忆压缩 | `DRY_RUN=true ./memory-compact.sh` |
| `memory-weekly-report.sh` | 生成周报 | `./memory-weekly-report.sh` |
| `memory-monitor.sh` | 监控主脚本 | `./memory-monitor.sh` |
| `send-feishu-message.sh` | 飞书推送 | `echo '消息' \| ./send-feishu-message.sh` |

---

## 📅 执行时间表

### 每周任务
```
周日 23:00 ─┬─ 记忆备份
            │
周一 09:00 ─┼─ 记忆健康监控
            │
周一 09:30 ─┴─ 周报生成与推送 ← 你在这里收到消息
```

### 每月任务
```
每月 1 号 10:00 ── 记忆维护
```

---

## 📈 监控仪表板（待实现）

未来可以添加：
- [ ] Web 仪表板展示任务执行历史
- [ ] Grafana 集成（如果有监控系统）
- [ ] Slack/飞书机器人实时状态

---

## 🔗 相关文档

- [HEARTBEAT.md](../HEARTBEAT.md) - 心跳任务配置
- [MEMORY-COMPACT-GUIDE.md](./MEMORY-COMPACT-GUIDE.md) - 记忆压缩指南
- [memory/reports/](./reports/) - 周报目录
- [memory/task-logs/](./task-logs/) - 任务日志目录

---

**创建时间**: 2026-03-28  
**最后审查**: 2026-03-28  
**下次审查**: 2026-04-04
