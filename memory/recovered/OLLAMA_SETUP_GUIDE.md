# 🚨 重要：Ollama 安装指引

## 问题现状

OpenClaw 记忆系统向量嵌入功能损坏，原因：`node-llama-cpp` 依赖缺失。

**影响时间**: 2026-03-10 至 2026-03-28（18 天）

---

## ✅ 已完成

- [x] 恢复 8 个会话记录（Markdown 格式）
- [x] 创建备份摘要文档
- [x] Git 暂存恢复文件

**备份位置**: `/home/rskuser/.openclaw/workspace/memory/recovered/`

---

## 🔧 需要执行的步骤（按顺序）

### 步骤 1：安装 Ollama（需要 sudo 密码）

**方法 A：一键安装脚本（推荐）**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**方法 B：手动下载**
1. 访问 https://ollama.ai/download
2. 下载 Linux 版本
3. 解压并移动到 `/usr/local/bin/`

**方法 C：Docker（无需 sudo）**
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

---

### 步骤 2：拉取嵌入模型

安装完成后执行：
```bash
# 推荐模型（平衡速度和准确度）
ollama pull nomic-embed-text

# 或更小的模型（速度更快）
ollama pull mxbai-embed-large
```

预计下载大小：~200MB

---

### 步骤 3：修改 OpenClaw 配置

编辑文件：`/home/rskuser/.openclaw/openclaw.json`

找到 `agents.defaults.memorySearch` 部分，修改为：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "ollama",
        "model": "nomic-embed-text",
        "store": {
          "driver": "sqlite",
          "path": "/home/rskuser/.openclaw/memory/main.sqlite",
          "vector": {
            "enabled": true
          }
        },
        "sync": {
          "onSessionStart": true,
          "watch": true,
          "intervalMinutes": 30
        },
        "query": {
          "maxResults": 5,
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3
          }
        },
        "cache": {
          "enabled": true
        },
        "remote": {
          "baseUrl": "http://localhost:11434"
        }
      }
    }
  }
}
```

**关键修改**:
- `provider`: `"local"` → `"ollama"`
- 添加 `remote.baseUrl`: `"http://localhost:11434"`

---

### 步骤 4：重启 OpenClaw Gateway

```bash
openclaw gateway restart
```

等待 10-20 秒后验证：

```bash
openclaw memory status
```

---

### 步骤 5：验证记忆功能

```bash
# 测试记忆搜索
openclaw memory search "记忆系统"

# 测试记忆读取
openclaw memory get memory/recovered/BACKUP_SUMMARY.md
```

---

## 🎯 快速验证清单

- [ ] Ollama 安装成功
  ```bash
  ollama --version
  ```

- [ ] 模型下载完成
  ```bash
  ollama list
  ```

- [ ] Ollama 服务运行中
  ```bash
  curl http://localhost:11434/api/tags
  ```

- [ ] OpenClaw 配置已更新
  ```bash
  cat /home/rskuser/.openclaw/openclaw.json | grep -A 5 '"provider"'
  ```

- [ ] Gateway 已重启
  ```bash
  ps aux | grep openclaw
  ```

- [ ] 记忆搜索正常
  ```bash
  openclaw memory search "测试"
  ```

---

## 📞 问题排查

### Q1: Ollama 安装失败
**解决**: 使用 Docker 方法（见步骤 1 方法 C）

### Q2: 模型下载慢
**解决**: 使用国内镜像或更换小模型
```bash
ollama pull mxbai-embed-large  # 更小更快
```

### Q3: OpenClaw 仍报错
**解决**: 检查配置 JSON 格式
```bash
jq . /home/rskuser/.openclaw/openclaw.json > /dev/null && echo "JSON 格式正确"
```

### Q4: 记忆搜索返回空结果
**解决**: 等待索引重建（首次需要几分钟）
```bash
# 查看索引状态
openclaw memory status
```

---

## 📊 预期效果

修复后：
- ✅ 语义检索恢复正常
- ✅ 新对话自动保存到记忆
- ✅ 支持混合检索（向量 + 关键词）
- ✅ 时间衰减和 MMR 去重生效

---

**创建时间**: 2026-03-28 14:22  
**执行状态**: 等待用户确认安装 Ollama
