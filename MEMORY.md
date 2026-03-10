# MEMORY.md - 长期记忆

## 🔴 红线规则（严格执行）

### 规则一：严禁删除
**未经过杨荣允许，严禁删除任何文件或软件。**

- 任何删除操作前必须明确征得同意
- 适用于：文件、文件夹、软件、技能、配置等一切删除行为
- 理由：尊重用户对系统和数据的完全控制权

### 规则二：严禁擅自发布代码
**未经过杨荣允许，严禁发布任何代码、配置或信息到 GitHub、ClawHub 或任何外部平台。**

- 适用于：代码、配置文件、API 密钥、技能包、数据分析结果等一切内容
- 发布前必须明确征得同意
- 理由：保护代码知识产权和数据安全

### 规则三：Skill 安全审查流程（2026-03-05 起执行）
**安装 Skill 必须执行两级扫描：**

#### 第一阶段：安装前快速扫描（clawVet）
- **工具**: clawVet
- **时机**: 安装任何 Skill 之前
- **作用**: 快速扫描代码，识别明显风险
- **检查项**: 可疑网络请求、文件读写、环境变量访问
- **结果处理**: 
  - 通过 → 进入安装流程
  - 不通过 → 禁止安装，报告用户

#### 第二阶段：安装后深度审查（clawVet）
- **工具**: clawVet（唯一工具，已包含完整功能）
- **时机**: 安装完成后立即执行
- **作用**: 深度代码审计，详细权限分析
- **评级**:
  - A/B 级（0-24 分）🟢：可正常使用
  - C 级（25-49 分）🟡：需用户二次确认
  - D 级（50-84 分）🟡：需用户特批
  - F 级（85-100 分）🔴：禁止安装，立即卸载
- **结果记录**: 写入 `SKILL_SECURITY_REPORT.md`

#### 第三阶段：100/3 法则验证
- **下载量**: 100 次以上（低于 100 → 禁止安装）
- **发布历史**: 3 个月以上（低于 3 个月 → 需用户特批）
- **异常检测**: 刚上线三天就有 500 下载 → 刷量嫌疑，禁止安装

#### 审批流程
```
用户提出安装需求
    ↓
clawVet 快速扫描（安装前）
    ↓
100/3 法则验证
    ↓
用户确认（如需特批）
    ↓
执行安装
    ↓
clawVet 深度审查（安装后）
    ↓
记录评级到 SKILL_SECURITY_REPORT.md
    ↓
完成
```

#### 中等风险技能使用流程（2026-03-05 10:13 决策）

**适用对象**: C/D 级技能（风险分 25-84/100）

```
用户提出使用需求
    ↓
我提示风险（显示风险分 + 主要问题）
    ↓
用户明确确认（"确认使用" / "yes" / 等）
    ↓
执行技能
    ↓
记录使用日志到 SKILL_WHITELIST.md
```

**当前中等风险技能清单**（6 个）:
- coding-agent (64/100 - D 级)
- 1password (48/100 - C 级)
- oracle (37/100 - C 级)
- notion (30/100 - C 级)
- summarize (30/100 - C 级)
- himalaya (28/100 - C 级)

---

### 规则四：回答不显示 Tool 调用（2026-03-05 10:17 起执行）
**默认行为：不在回答中显示工具调用过程**

- **原则**: 用户关心的是结果，不是过程
- **默认**: 直接给出答案/结果，不显示"我正在使用 XX 工具"
- **例外**: 
  - 用户明确询问"你是怎么做的"
  - 需要解释复杂操作流程
  - 调试/教学场景
- **理由**: 提升用户体验，避免技术细节干扰

**示例**:
- ❌ "我正在使用 clawvet audit 扫描技能..."
- ✅ "扫描完成！共检查 48 个技能，发现 88 个问题。"

---

## 📦 技能安装进度（2026-03-03）

### ✅ 已完成
- 复制 22 个技能文件到 `workspace/skills/`
- npm 安装 `oracle` CLI
- npm 安装 `jq`
- 创建 `deepanalyze` 数据分析技能

### 📊 DeepAnalyze 技能
- **模型**: custom-aigw-fx-ctripcorp-com-3/DeepAnalyze-8B
- **用途**: 专业数据分析、可视化、建模
- **工作流**: Analyze → Understand → Code → Execute → Answer
- **位置**: `workspace/skills/deepanalyze/`

### ⏳ 等待配置（5 个）
需要运行 `openclaw configure --section channels` 配置：
- discord (Bot Token)
- slack (Bot Token)
- voice-call (启用插件)
- bluebubbles (服务器配置)
- trello (API Key + Token 环境变量)

### ❌ 需要额外工具（11 个）
- 需要安装 Go: blogwatcher, wacli
- 需要安装 gh CLI: gh-issues
- macOS 专属（Windows 不可用）: camsnap, goplaces, openhue, sag, summarize, tmux
- 需要额外配置: coding-agent, sherpa-onnx-tts, himalaya, sonoscli

### 📄 详细状态
见 `SKILLS_SETUP.md`

---

## 待办与项目

### ✅ 已完成 (2026-03-10)

**OpenClaw 记忆系统 Git 版本控制配置**

- [x] 创建 `.gitignore` 保护敏感信息
- [x] 更新 `openclaw.json` 添加记忆系统配置
- [x] 创建 `memory/README.md` 版本控制指南
- [x] Git 首次提交 (ec75781)
- [x] 添加远程仓库 origin: https://github.com/juyangrong/openclaw-memory.git

**待完成**:
- [ ] 在 GitHub 创建仓库 `juyangrong/openclaw-memory` (需杨荣操作)
- [ ] 推送代码到远程仓库
- [ ] 重启 OpenClaw Gateway 使配置生效

### 📋 配置详情

**记忆系统配置**:
- 启用混合检索 (FTS + Vector)
- 向量权重 70%, 文本权重 30%
- 启用 MMR 去重
- 会话启动时自动同步
- 文件监听自动同步 (30 分钟间隔)
- Session Memory Hook 启用 (归档 15 条消息)

**Git 保护规则**:
- ❌ 严禁提交：openclaw.json, memory/*.sqlite, .openclaw/sessions/
- ✅ 允许提交：MEMORY.md, memory/*.md, AGENTS.md, SOUL.md, USER.md

详见 `记忆系统配置状态报告.md`

## 重要决策

_暂无_

## 个人上下文

_暂无_
