# GitHub CLI 快速参考

**版本**: gh 2.87.3  
**认证用户**: juyangrong  
**配置日期**: 2026 年 3 月 10 日

---

## 🚀 快速启动

### 当前会话使用
```powershell
# 临时添加 PATH (当前会话有效)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 或者直接使用完整路径
& "C:\Program Files\GitHub CLI\gh.exe" --version
```

### 永久配置
```powershell
# 运行配置脚本
.\setup-gh-path.ps1

# 然后重启 PowerShell
```

---

## 🔐 认证状态

```bash
# 查看认证状态
gh auth status

# 重新认证
gh auth login

# 注销
gh auth logout
```

**当前状态**: ✅ 已认证到 github.com (juyangrong)

---

## 📦 仓库管理

### 查看仓库
```bash
# 查看仓库信息
gh repo view juyangrong/openclaw-memory

# 查看仓库列表
gh repo list juyangrong

# 创建仓库
gh repo create my-new-repo --private
```

### 克隆仓库
```bash
# 克隆仓库
gh repo clone juyangrong/openclaw-memory
```

---

## 🔀 Pull Requests

### 查看 PR
```bash
# 列出 PR
gh pr list --repo juyangrong/openclaw-memory

# 查看 PR 详情
gh pr view 1 --repo juyangrong/openclaw-memory

# 查看 PR 检查状态
gh pr checks 1 --repo juyangrong/openclaw-memory
```

### 创建 PR
```bash
# 创建 PR
gh pr create --title "功能：添加新功能" --body "描述更改内容"

# 审查 PR
gh pr review --approve
gh pr review --comment --body "一些建议"
```

---

## 🐛 Issues

### 查看 Issue
```bash
# 列出 issue
gh issue list --repo juyangrong/openclaw-memory

# 查看详情
gh issue view 1 --repo juyangrong/openclaw-memory

# 查看带 JSON 输出
gh issue list --json number,title,state --jq '.[] | "\(.number): \(.title)"'
```

### 创建 Issue
```bash
# 创建 issue
gh issue create --title "问题描述" --body "详细描述"

# 添加标签
gh issue create --label "bug" --label "help wanted"
```

---

## ⚙️ GitHub Actions

### 查看工作流
```bash
# 列出工作流运行
gh run list --repo juyangrong/openclaw-memory --limit 10

# 查看运行详情
gh run view <run-id> --repo juyangrong/openclaw-memory

# 查看失败日志
gh run view <run-id> --repo juyangrong/openclaw-memory --log-failed

# 重新运行
gh run rerun <run-id> --repo juyangrong/openclaw-memory
```

### 监控 CI
```bash
# 实时监控
gh run watch <run-id> --repo juyangrong/openclaw-memory
```

---

## 🔍 高级查询 (API)

```bash
# 获取用户信息
gh api user --jq '.login, .name'

# 获取仓库信息
gh api repos/juyangrong/openclaw-memory --jq '.name, .stargazers_count'

# 获取 PR 列表
gh api repos/juyangrong/openclaw-memory/pulls --jq '.[] | {number, title}'

# 获取 issue 评论
gh api repos/juyangrong/openclaw-memory/issues/1/comments --jq '.[] | {user, body}'
```

---

## 📊 常用组合命令

### 检查仓库状态
```bash
# 一键检查
gh repo view && gh pr list && gh issue list
```

### 发布新版本
```bash
# 创建 release
gh release create v1.0.0 --title "v1.0.0" --notes "发布说明"
```

### Gist 管理
```bash
# 创建 gist
gh gist create file.txt

# 列出 gist
gh gist list
```

---

## 🔧 故障排查

### 问题：`gh` 命令找不到
**解决**:
```powershell
# 方法 1: 使用完整路径
& "C:\Program Files\GitHub CLI\gh.exe" --version

# 方法 2: 添加 PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 方法 3: 运行配置脚本
.\setup-gh-path.ps1
```

### 问题：认证失败
**解决**:
```bash
# 重新认证
gh auth logout
gh auth login
```

### 问题：权限不足
**解决**:
```bash
# 刷新 token
gh auth refresh --scopes repo,workflow,read:org
```

---

## 📚 相关资源

- **官方文档**: https://cli.github.com/manual/
- **GitHub 仓库**: https://github.com/cli/cli
- **认证**: `gh help auth`
- **所有命令**: `gh help`

---

## 🎯 OpenClaw 集成

OpenClaw 已有 `skills/github/SKILL.md`，可以直接使用：

```bash
# 在 OpenClaw 中使用
gh pr checks 55 --repo juyangrong/openclaw-memory
gh run list --repo juyangrong/openclaw-memory --limit 10
gh run view <run-id> --repo juyangrong/openclaw-memory --log-failed
```

---

*最后更新：2026 年 3 月 10 日*
