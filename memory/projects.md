# projects.md - 项目信息

_记录项目相关信息（重要性 4-5 分）_

---

## 项目列表

### 景德镇 + 婺源 + 望仙谷亲子游攻略
- **状态：** ✅ 已完成
- **日期：** 2026-03-15
- **描述：** 6 天 5 晚春假亲子游完整攻略（2 大 2 小，蔚来 ES6 自驾）
- **关键信息：**
  - 行程：景德镇（陶溪川、古窑、丙丁柴窑、瑶里古镇）+ 婺源（篁岭、江岭油菜花）+ 望仙谷（仙侠夜景）
  - 淘汰 14 个景点（季节不符/路程远/亲子适应性差/景观重复）
  - 预算：6000-11200 元（经济/舒适/豪华三档）
  - 输出：MD 文档 + PDF 攻略（10-12 页，32 张配图）+ GitHub 仓库
  - 注意事项：4 月油菜花最佳期、提前 2-3 周订酒店、江西菜偏辣、陶瓷博物馆需预约
- **最后更新：** 2026-03-23

### 定时任务系统配置
- **状态：** 🟢 已完成
- **开始日期：** 2026-03-20
- **描述：** 配置 OpenClaw 的长期记忆整理定时任务
- **关键信息：** 
  - HEARTBEAT.md 任务清单（每日/每周/每月检查）
  - 系统 cron：每天 09:00 和 20:00 执行
  - 脚本位置：`~/.openclaw/scripts/heartbeat.sh`
  - 状态追踪：`memory/heartbeat-state.json`
  - 测试执行：成功
- **最后更新：** 2026-03-20

### 技能扩展
- **状态：** 🟢 进行中
- **开始日期：** 2026-03-20
- **描述：** 安装和配置实用 skills
- **关键信息：**
  - skill-vetter-1-0-0：技能审查工具
  - browser-automation：浏览器自动化（Playwright）
  - self-improving-proactive-agent：自我改进主动代理
  - feishu_cursor_cc_orchestrator：飞书×Cursor RIPER-5 编排技能（2026-03-26 安装）
- **最后更新：** 2026-03-26

### Job Dependency Analyzer Skill
- **状态：** 🟢 已完成（待 MCP 工具调试）
- **日期：** 2026-03-23
- **描述：** 基于 Zeus MCP 和 Metadata MCP 的作业依赖分析工具
- **关键信息：**
  - 功能：分析作业依赖关系、生成 Mermaid 流程图、发布到飞书文档
  - MCP 服务器：Zeus MCP（作业编排）+ Metadata MCP（表元数据）
  - 脚本：analyze_job_dependency.py、update_feishu_doc.py、main.py、discover_mcp_tools.py
  - 发现：MCP 使用 mcp-session-id 头进行会话管理
  - 待办：tools/list 参数问题需要调试
- **最后更新：** 2026-03-23

### Feishu Cursor CC Orchestrator Skill v2
- **状态：** 🟢 已完成（轮询模式 v2）
- **日期：** 2026-03-26
- **描述：** 飞书群任务编排器，支持多群监听，动态回复
- **关键信息：**
  - **功能：** 监听 /oc-dev 指令 → @ Cursor 机器人 → 发送任务 → RIPER-5 协议执行
  - **方案：** API 轮询模式（无需 webhook，无需修改插件代码）
  - **v2 新特性：**
    - 配置独立化：config.json 管理 cursorBot 配置
    - 多群监听：自动监听所有群或指定群
    - 动态回复：在收到消息的群里自动回复
    - 内存优化：自动清理旧消息记录（保留 1000 条）
  - **配置：** `config.json` - cursorBot, wakePrefix, pollInterval, chatIds
  - **需要权限：** `im:message.group_msg`（飞书开放平台配置）
  - **Cursor 机器人：** `yr.ju 的 cursor 编程助手` (`ou_5d92ec453c78e7bfd6c43c8d685c1982`)
  - **启动命令：** `node scripts/polling-listener.js`
  - **日志：** `/tmp/cursor-orchestrator-v2.log`
- **最后更新：** 2026-03-26

### 记忆系统恢复
- **状态：** ✅ 已完成
- **日期：** 2026-03-28
- **描述：** 修复本地向量嵌入系统，恢复记忆同步功能
- **关键信息：**
  - **问题：** `node-llama-cpp` 依赖缺失导致记忆同步停止 18 天（3/10-3/28）
  - **解决方案：** 安装 Ollama 0.18.3（CPU-only）+ nomic-embed-text 模型（274MB）
  - **配置更新：** `/home/rskuser/.openclaw/openclaw.json` 设置 memorySearch.provider = "ollama"
  - **会话恢复：** 8 个 JSONL 会话文件恢复为 Markdown（450 条消息，78KB）
  - **恢复脚本：** `/tmp/recover-sessions.sh` → `/home/rskuser/.openclaw/workspace/memory/recovered/`
  - **Git 提交：** `fe3dc82` - "feat(memory): 恢复 2026-03-17 至 2026-03-28 的会话记录"
- **经验教训：**
  - 定期监控记忆系统状态（每周检查 `openclaw memory status`）
  - 配置会话记录自动备份（定期导出 JSONL 到 Markdown）
  - 安装后验证 `node-llama-cpp` 状态
- **最后更新：** 2026-04-06（从 2026-03-28.md 日志提炼）

---

_项目状态定期更新，完成后归档_
