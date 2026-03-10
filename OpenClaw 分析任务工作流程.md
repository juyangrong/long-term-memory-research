# OpenClaw 分析任务工作流程

**创建日期**: 2026 年 3 月 10 日  
**用途**: 记录 OpenClaw 接收分析任务 → 生成报告 → 上传到 yang-analysis 的完整流程

---

## 📋 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│            OpenClaw 分析任务工作流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣  用户提出分析需求                                        │
│      │                                                      │
│      ▼                                                      │
│  2️⃣  OpenClaw 接收任务并执行分析                             │
│      │                                                      │
│      ▼                                                      │
│  3️⃣  生成分析报告 (.md 格式)                                 │
│      │                                                      │
│      ▼                                                      │
│  4️⃣  保存到 workspace                                       │
│      │                                                      │
│      ▼                                                      │
│  5️⃣  分类到 yang-analysis 对应目录                           │
│      │                                                      │
│      ▼                                                      │
│  6️⃣  Git 提交并推送到 GitHub                                  │
│      │                                                      │
│      ▼                                                      │
│  7️⃣  记录到 MEMORY.md (长期记忆)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 分类规则

### 01-AI 框架分析/
**适用**: AI 框架调研、技术对比、选型报告

**示例**:
- AI 代理框架技术方案深度对比报告.md
- LangChain 全面学习路径与前沿研究报告.md
- LangChain 替代方案对比分析报告.md

### 02-OpenClaw 系统/
**适用**: OpenClaw 配置、记忆系统、CLI 工具

**示例**:
- OpenClaw 记忆系统技术方案深度调研报告.md
- 记忆系统配置状态报告.md
- GitHub CLI 快速参考.md

### 03-Skill 安全/
**适用**: Skill 安全审查、风险评估、白名单

**示例**:
- SKILL_SECURITY_REPORT.md
- SKILL_INSTALL_SECURITY_PROCESS.md
- SKILL_WHITELIST.md

### 04-其他文档/
**适用**: 其他技术文档、工作计划

### 05-下载文档/
**适用**: 从 Downloads 目录收集的临时分析文档

---

## 🔧 操作步骤

### 步骤 1: 生成分析报告

OpenClaw 执行分析任务后，报告保存在：
```
D:\Users\yr.ju.CN1\.openclaw\workspace\分析报告.md
```

### 步骤 2: 分类复制

```powershell
# 根据报告类型选择目标目录
$reportName = "分析报告.md"
$targetDir = "D:\Users\yr.ju.CN1\.openclaw\workspace\yang-analysis\01-AI 框架分析\"

Copy-Item "$reportName" -Destination "$targetDir"
```

### 步骤 3: Git 提交

```powershell
cd "D:\Users\yr.ju.CN1\.openclaw\workspace\yang-analysis"

# 添加 PATH (如未配置)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 提交更改
git add .
git commit -m "docs: 添加新的分析报告 - <报告主题>"
git push origin master
```

### 步骤 4: 记录到 MEMORY.md

更新 `MEMORY.md` 的"重要决策"部分：

```markdown
### 分析报告上传 (YYYY-MM-DD)

- **报告名称**: 分析报告.md
- **分类目录**: 01-AI 框架分析/
- **GitHub 提交**: <commit-hash>
- **仓库 URL**: https://github.com/juyangrong/yang-analysis
```

---

## 📊 快速参考

### 仓库信息

| 项目 | 值 |
|------|-----|
| **仓库** | juyangrong/yang-analysis |
| **URL** | https://github.com/juyangrong/yang-analysis |
| **可见性** | 私有 (Private) |
| **用途** | 技术分析长期记忆库 |

### 常用命令

```bash
# 查看仓库状态
gh repo view juyangrong/yang-analysis

# 克隆仓库
gh repo clone juyangrong/yang-analysis

# 查看提交历史
git log --oneline -10

# 查看文件
git ls-tree -r master --name-only
```

---

## 🎯 示例场景

### 场景 1: AI 框架调研

**用户**: "帮我调研 LangChain 生态"

**流程**:
1. OpenClaw 执行调研，生成 `LangChain 生态调研报告.md`
2. 分类到 `01-AI 框架分析/`
3. Git 提交：`git commit -m "docs: 添加 LangChain 生态调研报告"`
4. 推送到 GitHub
5. 记录到 MEMORY.md

### 场景 2: 系统配置分析

**用户**: "分析 OpenClaw 记忆系统配置"

**流程**:
1. OpenClaw 生成 `OpenClaw 记忆系统配置分析.md`
2. 分类到 `02-OpenClaw 系统/`
3. Git 提交并推送
4. 记录到 MEMORY.md

### 场景 3: Skill 安全审查

**用户**: "审查新安装的 Skill"

**流程**:
1. OpenClaw 执行审查，生成 `SKILL_SECURITY_XXX.md`
2. 分类到 `03-Skill 安全/`
3. Git 提交并推送
4. 记录到 MEMORY.md

---

## 📝 更新日志

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-03-10 | 初始创建 | 建立工作流程文档 |
| 2026-03-10 | 首次执行 | 整理 25+ 个分析报告到 yang-analysis |

---

*本工作流程文档作为 OpenClaw 分析任务的标准操作指南*
