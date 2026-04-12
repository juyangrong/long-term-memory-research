# 记忆压缩指南

**最后更新**: 2026-03-28  
**维护者**: 贾维斯 🏠

---

## 📋 概述

记忆压缩是定期整理旧日志文件到长期记忆（MEMORY.md）的过程，防止日志文件无限增长。

**执行频率**: 每月 1 号  
**预计耗时**: 10-20 分钟（手动审查）  
**风险等级**: 🟡 低（保留原始文件）

---

## 🔧 工具

### 自动脚本
```bash
# 位置
/home/rskuser/.openclaw/workspace/scripts/memory-compact.sh

# 干运行（预览，不实际删除）
DRY_RUN=true ./scripts/memory-compact.sh

# 实际执行
DRY_RUN=false ./scripts/memory-compact.sh
```

### 脚本功能
1. **识别待整理文件** - 超过 7 天的日志
2. **统计信息** - 行数、词数
3. **清理过期文件** - 超过 30 天的日志（可选）
4. **生成日志** - `memory/compact-YYYY-MM-DD.log`

---

## 📝 手动压缩流程

### 步骤 1：运行脚本预览

```bash
cd /home/rskuser/.openclaw/workspace
DRY_RUN=true ./scripts/memory-compact.sh
```

查看输出，确认需要整理的文件列表。

### 步骤 2：阅读待整理文件

```bash
# 查看文件列表
ls -lht memory/2026-*.md | head -10

# 阅读具体内容
cat memory/2026-03-10.md
```

### 步骤 3：提炼关键信息

阅读文件后，识别以下类型的信息：

| 类型 | 重要性 | 存储位置 |
|------|--------|----------|
| **核心决策** | ⭐⭐⭐⭐⭐ | MEMORY.md → decisions.md |
| **用户偏好** | ⭐⭐⭐⭐ | MEMORY.md → preferences.md |
| **项目信息** | ⭐⭐⭐⭐ | MEMORY.md → projects.md |
| **联系人信息** | ⭐⭐⭐⭐ | MEMORY.md → contacts.md |
| **经验教训** | ⭐⭐⭐⭐ | MEMORY.md → patterns.md |
| **日常记录** | ⭐⭐ | 保留日志文件，30 天后删除 |

### 步骤 4：更新 MEMORY.md

手动将提炼的内容添加到 `MEMORY.md` 对应专题文件：

```markdown
## 📌 重要决策（decisions.md）

### 2026-03-10: 选择 Ollama 作为嵌入服务
- **决策**: 使用 Ollama 替代 node-llama-cpp
- **原因**: 稳定性更好，独立服务，模型可选
- **影响**: 记忆系统稳定性大幅提升
```

### 步骤 5：执行清理（可选）

确认信息已提炼后，执行实际清理：

```bash
DRY_RUN=false ./scripts/memory-compact.sh
```

**注意**: 脚本只删除超过 30 天的文件，7-30 天的文件保留。

### 步骤 6：Git 提交

```bash
cd /home/rskuser/.openclaw/workspace
git add memory/
git commit -m "chore(memory): 月度记忆压缩 - 整理 2026-03-XX 日志"
git push origin master
```

---

## ⚠️ 注意事项

### 安全原则
1. **先提炼，后删除** - 确保重要信息已保存到 MEMORY.md
2. **保留原始文件** - 7-30 天的文件不删除
3. **Git 版本控制** - 每次修改后提交
4. **DRY_RUN 优先** - 先预览，再执行

### 跳过压缩的情况
- 文件包含未完成的 project
- 有 pending 的决策需要后续跟进
- 用户明确要求保留

### 恢复误删除
```bash
# 从 Git 恢复
git checkout HEAD~1 -- memory/2026-03-XX.md

# 从 recovered 备份恢复
cp memory/recovered/2026-03-XX.md memory/
```

---

## 📊 压缩记录

| 日期 | 整理文件数 | 删除文件数 | 新增记忆条目 | 操作者 |
|------|------------|------------|--------------|--------|
| 2026-03-28 | 1 (预览) | 0 | - | 贾维斯 |

---

## 🔗 相关文档

- [HEARTBEAT.md](../HEARTBEAT.md) - 心跳任务配置
- [MEMORY.md](./MEMORY.md) - 核心知识库
- [scripts/memory-compact.sh](../scripts/memory-compact.sh) - 压缩脚本

---

**最后审查**: 2026-03-28  
**下次审查**: 2026-04-01
