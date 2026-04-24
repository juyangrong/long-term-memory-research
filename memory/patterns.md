# patterns.md - 模式和最佳实践

_记录重复出现的模式、经验教训和最佳实践（重要性 4-5 分）_

---

## 模式库

### 双层记忆架构
- **类别：** 工作流
- **适用场景：** 会话重启后保持记忆连续性
- **实践方法：**
  - 短期记忆：memory/YYYY-MM-DD.md 每日日志（30 天衰减）
  - 长期记忆：MEMORY.md + 专题文件（contacts/decisions/preferences/projects/patterns/feedback）
  - 每周一 09:00 执行 consolidation：将上周每日日志提炼到专题文件
  - 每月 1 号审查 MEMORY.md，移除过时信息
- **注意事项：** 重要性评分 1-5 分，≥4 分才进入长期记忆
- **最后更新：** 2026-03-23

### Heartbeat 主动检查机制
- **类别：** 工作流
- **适用场景：** 定期后台任务执行，无需用户触发
- **实践方法：**
  - HEARTBEAT.md 维护任务清单（每日/每周/每月）
  - 系统 cron 每天 09:00 和 20:00 触发
  - 状态追踪：memory/heartbeat-state.json 记录上次检查时间
  - 无事时回复 HEARTBEAT_OK，有事时直接报告
- **注意事项：** 避免频繁检查（间隔≥30 分钟），深夜 23:00-08:00 保持安静
- **最后更新：** 2026-03-23

### 记忆检索机制
- **类别：** 技术架构
- **适用场景：** 回答用户问题前自动检索相关记忆，确保回复基于完整上下文
- **实践方法：**
  - **混合检索：** BM25 关键词匹配 + 向量语义搜索，兼顾精确匹配和语义理解
  - **本地 Embedding：** Ollama + nomic-embed-text 模型，无需外部 API
  - **检索范围：** MEMORY.md + memory/*.md 专题文件 + 可选会话转录
  - **时间衰减：** 30 天周期，近期内容（memory/YYYY-MM-DD.md）权重更高
  - **触发时机：** 每次回答前自动执行，尤其是涉及 prior work/decisions/dates/people/preferences/todos 的问题
  - **引用格式：** 低置信度时说明"checked memory"，需要时使用 Source: <path#line> 标注来源
- **注意事项：** 
  - 检索是 mandatory 步骤，不可跳过
  - 检索后使用 memory_get 仅拉取需要的行，保持上下文精简
  - 如果 memory_search 返回 disabled=true，需向用户说明记忆检索不可用
- **最后更新：** 2026-03-24

### 记忆系统恢复流程
- **类别：** 故障恢复
- **适用场景：** 向量嵌入系统失效导致记忆同步停止
- **症状识别：**
  - 短期记忆多日未更新（检查 memory/YYYY-MM-DD.md 最新日期）
  - `openclaw memory status` 显示嵌入服务异常
  - 会话重启后无法检索历史记忆
- **恢复步骤：**
  1. **诊断根因：** 检查 `node-llama-cpp` 依赖状态或嵌入服务日志
  2. **安装 Ollama：** `curl -fsSL https://ollama.ai/install.sh | sh`（CPU-only 或 GPU 版本）
  3. **下载嵌入模型：** `ollama pull nomic-embed-text`（274MB，推荐平衡速度与准确度）
  4. **更新配置：** `/home/rskuser/.openclaw/openclaw.json` 设置 `memorySearch.provider = "ollama"`，`baseUrl = "http://localhost:11434"`
  5. **备份会话：** 导出 JSONL 会话文件到安全位置（防止数据丢失）
  6. **恢复历史记录：** 编写脚本将 JSONL 转换为 Markdown 存入 `memory/recovered/`
  7. **重启 Gateway：** 验证记忆搜索功能正常
  8. **验证测试：** 执行记忆检索测试，确认混合检索生效
- **注意事项：**
  - 修复前先手动备份所有会话记录
  - 选择 Ollama 而非重装 OpenClaw（减少破坏性变更）
  - 恢复后定期监控记忆系统状态（每周检查）
- **最后更新：** 2026-04-06（从 2026-03-28.md 日志提炼）

---

_模式定期回顾和更新，淘汰过时的实践_
