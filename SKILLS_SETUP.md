# 技能安装与配置状态

_最后更新：2026-03-03 15:15_

## ✅ 已就绪（6 个）

| 技能 | 状态 | 备注 |
|------|------|------|
| github | ✅ | 已就绪 |
| healthcheck | ✅ | 已就绪 |
| skill-creator | ✅ | 已就绪 |
| weather | ✅ | 已就绪 |
| oracle | ✅ | npm 安装完成 |
| jq | ✅ | npm 安装完成 |

## ⏳ 已复制技能文件，等待配置（5 个）

这些技能的文件已复制到 `skills/` 目录，但需要配置才能使用：

| 技能 | 需要配置 | 说明 |
|------|----------|------|
| discord | `channels.discord.token` | Discord Bot Token |
| slack | `channels.slack` | Slack Bot Token |
| voice-call | `plugins.entries.voice-call.enabled` | 启用语音通话插件 |
| bluebubbles | `channels.bluebubbles` | BlueBubbles 服务器配置 |
| trello | `TRELLO_API_KEY`, `TRELLO_TOKEN` | 环境变量 |

## ❌ 需要额外安装 CLI 工具（11 个）

这些技能需要安装对应的 CLI 工具：

### Windows 可安装
| 技能 | 安装方式 | 备注 |
|------|----------|------|
| blogwatcher | `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest` | 需要先安装 Go |
| gh-issues | `gh` CLI | GitHub CLI，需要认证 |
| himalaya | 查看技能文档 | 邮件客户端 |
| sonoscli | 查看技能文档 | Sonos 音响控制 |
| wacli | `go install github.com/steipete/wacli/cmd/wacli@latest` | 需要先安装 Go |

### macOS 专属（Windows 不可用）
| 技能 | 原因 |
|------|------|
| camsnap | 需要 brew |
| goplaces | 需要 brew + Google Places API Key |
| openhue | 需要 brew |
| sag | 需要 brew + ElevenLabs API Key |
| summarize | 需要 brew |
| tmux | macOS/Linux only |

### 需要额外配置
| 技能 | 需要 |
|------|------|
| coding-agent | claude/codex/opencode/pi 任一 |
| sherpa-onnx-tts | SHERPA_ONNX_RUNTIME_DIR, SHERPA_ONNX_MODEL_DIR |

---

## 下一步操作

### 立即可配置（无需安装）
1. **Discord** - 配置 Bot Token
2. **Slack** - 配置 Bot Token
3. **Voice-call** - 启用插件
4. **Trello** - 设置 API Key 和 Token

### 需要安装 Go 后可安装
1. `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`
2. `go install github.com/steipete/wacli/cmd/wacli@latest`

### 需要安装 GitHub CLI
```bash
winget install GitHub.cli
gh auth login
```

---

## 技能文件位置

所有技能文件已复制到：
`D:\Users\yr.ju.CN1\.openclaw\workspace\skills\`

共 22 个技能：
- blogwatcher, bluebubbles, camsnap, canvas
- coding-agent, discord, gh-issues, github
- goplaces, himalaya, imsg, openhue
- oracle, sag, sherpa-onnx-tts, slack
- sonoscli, summarize, tmux, trello
- voice-call, wacli
