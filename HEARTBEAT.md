# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## 🫀 记忆系统健康监控（每周执行）

### 检查频率
- **时间**: 每周一 09:00（Asia/Shanghai）
- **执行**: Heartbeat 会话自动触发
- **日志记录**: 执行后调用 `log-task.sh` 记录状态

---

## 📊 周报生成与推送（每周执行）

### 检查频率
- **时间**: 每周一 09:30（Asia/Shanghai）
- **执行**: Heartbeat 会话自动触发

### 执行清单

#### 1. 生成周报
```bash
cd /home/rskuser/.openclaw/workspace
./scripts/memory-monitor.sh
```

#### 2. 推送飞书消息
使用 `feishu_im_user_message` 工具发送周报摘要：
- **接收者**: `ou_b148c321fa9f39bda5a30abab40118d7`（杨荣）
- **消息类型**: `text`
- **内容**: 周报前 50 行摘要 + 完整报告链接

#### 3. 记录执行状态
```bash
./scripts/log-task.sh "weekly-report" "success" "周报已推送"
```

### 推送内容模板
```
【定时任务周报 - 2026-W12】

📊 执行摘要
- 总执行次数：X
- 成功率：XX%

📋 任务详情
| 任务 | 成功 | 失败 | 成功率 |
|------|------|------|--------|
| ...  | ...  | ...  | ...    |

💡 建议
...

完整报告：memory/reports/weekly-report-2026-W12.md
```

### 检查清单

#### 1. OpenClaw 记忆状态
```bash
openclaw memory status 2>&1 | head -20
```
**预期**: 返回正常，无 "Local embeddings unavailable" 错误

#### 2. Ollama 服务状态
```bash
curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null
```
**预期**: 返回 `nomic-embed-text:latest`

#### 3. 记忆文件完整性
```bash
ls -lh /home/rskuser/.openclaw/workspace/memory/*.md 2>/dev/null | tail -5
```
**预期**: 存在最近的记忆文件

### 异常处理
- 如果 Ollama 服务未响应 → 尝试 `systemctl restart ollama`
- 如果记忆状态报错 → 记录到 memory/diagnostic-YYYY-MM-DD.md
- 如果连续 2 周失败 → 通知用户

---

## 🧹 记忆维护（每月 1 号执行）

### 检查频率
- **时间**: 每月 1 号 10:00（Asia/Shanghai）

### 维护清单

#### 1. 整理旧日志到长期记忆
- 读取 `memory/YYYY-MM-DD.md` 文件（超过 7 天）
- 提取关键信息更新到 `MEMORY.md` 对应专题
- 记录整理结果

#### 2. 清理过期文件
- 删除超过 30 天的 `memory/YYYY-MM-DD.md` 文件
- 保留最近的 30 个日志文件

#### 3. 验证备份
- 检查 `memory/recovered/` 目录完整性
- 确认 Git 仓库已推送

---

## 💾 记忆备份（每周日 23:00 执行）

### 检查频率
- **时间**: 每周日 23:00（Asia/Shanghai）

### 备份清单

#### 执行备份脚本
```bash
cd /home/rskuser/.openclaw/workspace
./scripts/memory-backup.sh
```

#### 验证备份
- 检查 `memory/backups/YYYY-Www/` 目录
- 确认 BACKUP_INFO.md 已创建
- 验证 Git 提交成功

### 保留策略
- **保留周期**: 12 周（约 3 个月）
- **存储位置**: `memory/backups/`
- **格式**: 完整文件复制 + 元数据
