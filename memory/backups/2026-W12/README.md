# OpenClaw 记忆系统版本控制指南

**仓库**: https://github.com/juyangrong/openclaw-memory.git  
**最后更新**: 2026 年 3 月 10 日  
**负责人**: 杨荣

---

## 📋 目录结构

```
openclaw-memory/
├── .gitignore                    # Git 忽略配置（敏感信息保护）
├── README.md                     # 本文件
├── MEMORY.md                     # 长期记忆（curated）
├── memory/                       # 日常记忆日志
│   ├── README.md                 # 记忆目录说明
│   ├── YYYY-MM-DD.md            # 每日日志
│   └── heartbeat-state.json     # 心跳状态
├── AGENTS.md                     # Agent 行为准则
├── SOUL.md                       # 身份定义
├── USER.md                       # 用户信息
├── HEARTBEAT.md                  # 心跳配置
└── TOOLS.md                      # 工具配置
```

---

## 🔐 安全规则（严格执行）

### 红线规则

**未经过杨荣允许，严禁提交以下内容：**

1. ❌ **API 密钥和配置文件**
   - `openclaw.json`（包含 API 密钥）
   - `.env` 文件
   - 任何包含密钥的配置文件

2. ❌ **数据库文件**
   - `memory/*.sqlite`
   - `*.db` 文件
   - 向量索引文件

3. ❌ **敏感个人信息**
   - 身份证号、银行卡号
   - 健康医疗信息
   - 财务信息

4. ❌ **会话转录**
   - `.openclaw/sessions/`
   - `.openclaw/transcripts/`

### 允许提交的内容

✅ **记忆文件**（核心追踪内容）:
- `MEMORY.md` - 长期记忆
- `memory/*.md` - 日常日志
- `AGENTS.md`, `SOUL.md`, `USER.md` - 身份配置
- `HEARTBEAT.md`, `TOOLS.md` - 配置

✅ **文档和报告**:
- 技术调研报告
- 学习总结
- 项目文档

---

## 📝 Git 工作流程

### 日常提交

```bash
# 1. 查看状态
git status

# 2. 添加记忆文件
git add MEMORY.md
git add memory/*.md

# 3. 提交
git commit -m "docs(memory): 更新长期记忆 - 2026-03-10"

# 4. 推送到远程
git push origin master
```

### 定期整理（建议每周）

```bash
# 1. 审查记忆文件
# 阅读 MEMORY.md 和 memory/ 目录，删除过时信息

# 2. 整理提交
git add MEMORY.md
git commit -m "docs(memory): 整理长期记忆，删除过时信息"

# 3. 推送
git push origin master
```

### 敏感信息检查（提交前必做）

```bash
# 1. 查看将要提交的内容
git diff --cached

# 2. 检查是否包含敏感词
git diff --cached | Select-String -Pattern "sk-|api[_-]?key|password|secret|token"

# 3. 确认无误后提交
```

---

## 🔄 记忆文件管理规范

### MEMORY.md 管理

**更新频率**: 按需更新，定期整理（每周/每月）

**内容类型**:
- 重要决策和教训
- 长期项目和状态
- 安全规则和流程
- 技能安装进度

**整理原则**:
- 删除过时信息
- 合并重复内容
- 保持简洁清晰

### memory/*.md 管理

**更新频率**: 每日自动生成 + Session Hook 自动归档

**文件命名**:
- `YYYY-MM-DD.md` - 每日日志
- `YYYY-MM-DD-slug.md` - Session Hook 生成的会话归档

**保留策略**:
- 每日日志：保留 30 天
- 会话归档：保留 90 天
- 重要会话：手动移动到 MEMORY.md

---

## 🛠️ 自动化脚本

### 备份脚本（PowerShell）

```powershell
# backup-memory.ps1
# 用途：备份记忆文件到本地备份目录

$backupDir = "D:\Backups\openclaw-memory"
$workspace = "D:\Users\yr.ju.CN1\.openclaw\workspace"
$date = Get-Date -Format "yyyy-MM-dd-HHmmss"

# 创建备份目录
New-Item -ItemType Directory -Force -Path $backupDir

# 复制记忆文件
Copy-Item "$workspace\MEMORY.md" "$backupDir\MEMORY-$date.md"
Copy-Item "$workspace\memory\*.md" "$backupDir\" -Force

Write-Host "备份完成：$backupDir"
```

### 定期清理脚本

```powershell
# cleanup-old-memory.ps1
# 用途：清理 90 天前的记忆日志

$memoryDir = "D:\Users\yr.ju.CN1\.openclaw\workspace\memory"
$cutoffDate = (Get-Date).AddDays(-90)

Get-ChildItem -Path $memoryDir -Filter "*.md" | Where-Object {
    $_.LastWriteTime -lt $cutoffDate -and $_.Name -match "^\d{4}-\d{2}-\d{2}.md"
} | Remove-Item -Force

Write-Host "清理完成：删除 90 天前的记忆日志"
```

---

## 📊 版本历史

| 日期 | 版本 | 更新内容 | 负责人 |
|------|------|----------|--------|
| 2026-03-10 | v1.0 | 初始版本：配置 Git 仓库、.gitignore、记忆系统配置 | 杨荣 |

---

## 🔗 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [OpenClaw 记忆系统调研报告](./OpenClaw 记忆系统技术方案深度调研报告.md)
- [长期记忆技术分析报告](./长期记忆技术分析报告.md)

---

## 📞 联系方式

如有疑问，请联系：
- **负责人**: 杨荣
- **GitHub**: https://github.com/juyangrong

---

*本文档遵循"红线规则"：未经杨荣允许，严禁删除任何文件或软件。*
