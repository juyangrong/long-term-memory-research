# Long-Term Memory Research for AI Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Update](https://img.shields.io/badge/last%20update-2026--03--14-blue.svg)](https://github.com/yrju/long-term-memory-research)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> 🧠 全面深入的 AI 长期记忆技术调研资料库 | Comprehensive Research on Long-Term Memory for AI Agents

**[中文文档](README.md)** | **[English Docs](docs/en/README_en.md)**

---

## 📖 项目简介

本项目是一个**系统化、结构化的 AI 长期记忆技术调研资料库**，涵盖从理论基础到落地实施的完整内容。

### 核心内容

- 🔬 **5 大技术方向**：向量记忆、图结构记忆、分层记忆、原生记忆、生物启发式记忆
- 🏢 **5 大应用场景**：客户服务、个人助理、教育、医疗健康、企业知识管理
- 🛠️ **2 套实施方案**：Python 环境 + Dify 工作流，含完整代码
- 📊 **4 大深度调研**：学术前沿、工业案例、开源对比、安全治理
- 🔄 **自动化更新**：每两天自动同步最新研究进展

### 适合人群

| 角色 | 推荐内容 | 预计收益 |
|------|----------|----------|
| **技术负责人** | 执行摘要 + 方案选型决策树 | 5 分钟掌握技术方向 |
| **开发者** | 技术方向 + Python 实施方案 | 1-2 周完成落地 |
| **产品经理** | 应用场景 + Dify 实施方案 | 2-3 天完成原型 |
| **研究者** | 学术前沿 + 开源对比 | 跟踪最新进展 |

---

## 🚀 快速开始

### 在线阅读

- 📖 [完整文档](docs/)
- 📊 [执行摘要](docs/00-执行摘要.md)
- 🛠️ [实施方案](docs/04-落地实施方案/)

### 本地使用

```bash
# 1. 克隆项目
git clone https://github.com/yrju/long-term-memory-research.git
cd long-term-memory-research

# 2. 查看文档
open docs/README.md  # macOS
xdg-open docs/README.md  # Linux
start docs/README.md  # Windows

# 3. (可选) 设置自动更新
./scripts/update.sh --setup-cron
```

### 决策树

```
是否需要长期记忆？
  ├─ 否 → 使用标准上下文窗口
  └─ 是
      ├─ 强监管行业？ → Python + 结构化记忆 + 审计
      └─ 否
          ├─ 技术团队？ → Python 方案 (1-2 周)
          └─ 产品团队？ → Dify 方案 (2-3 天)
```

---

## 📁 项目结构

```
long-term-memory-research/
├── README.md                           # 项目说明 (本文档)
├── LICENSE                             # MIT 许可
├── CONTRIBUTING.md                     # 贡献指南
├── docs/                               # 文档目录
│   ├── 00-执行摘要.md                  # 🚀 从这里开始
│   ├── 01-技术方向/                    # 5 篇技术文档
│   │   ├── 01-向量记忆技术.md
│   │   ├── 02-图结构记忆.md
│   │   ├── 03-分层记忆架构.md
│   │   ├── 04-原生记忆研究.md
│   │   └── 05-生物启发式记忆.md
│   ├── 02-应用场景/                    # 5 篇场景文档
│   │   ├── 01-客户服务场景.md
│   │   ├── 02-个人助理场景.md
│   │   ├── 03-教育场景.md
│   │   ├── 04-医疗健康场景.md
│   │   └── 05-企业知识管理.md
│   ├── 03-全网资料深度探索/            # 4 篇深度调研
│   │   ├── 01-学术研究前沿.md
│   │   ├── 02-工业界落地案例.md
│   │   ├── 03-开源项目对比.md
│   │   └── 04-安全与治理.md
│   ├── 04-落地实施方案/                # 3 篇实施方案
│   │   ├── 01-Python 环境实施方案.md
│   │   ├── 02-Dify 工作流实施方案.md
│   │   └── 03-方案选型决策树.md
│   └── 05-附录/                        # 3 篇附录
│       ├── 01-关键术语表.md
│       ├── 02-性能基准对比.md
│       └── 03-参考资料索引.md
├── scripts/                            # 自动化脚本
│   ├── update.sh                       # 更新入口
│   ├── update_research.py              # 更新逻辑
│   └── requirements.txt                # Python 依赖
├── examples/                           # 代码示例
│   ├── python/                         # Python 示例
│   │   ├── memory_service.py
│   │   ├── sensitive_filter.py
│   │   └── personal_assistant.py
│   └── dify/                           # Dify 工作流
│       └── memory_workflow.json
└── assets/                             # 图片资源
    └── diagrams/                       # 架构图
```

---

## 📊 核心结论

### 技术成熟度评估

| 技术方向 | 成熟度 | 生产就绪 | 推荐指数 |
|----------|--------|----------|----------|
| 向量记忆 | ⭐⭐⭐⭐⭐ | ✅ | 🔥 强烈推荐 |
| 分层记忆 | ⭐⭐⭐⭐⭐ | ✅ | 🔥 强烈推荐 |
| 图结构记忆 | ⭐⭐⭐⭐ | ✅ | 推荐 |
| 原生记忆 | ⭐⭐ | ❌ | 研究跟踪 |
| 生物启发式 | ⭐⭐ | ❌ | 研究跟踪 |

### 方案对比

| 方案 | 实施周期 | 成本 | 灵活性 | 适合团队 |
|------|----------|------|--------|----------|
| Python | 1-2 周 | $200-500/月 | ⭐⭐⭐⭐⭐ | 技术团队 |
| Dify | 2-3 天 | $0-50/月 | ⭐⭐⭐ | 产品团队 |

### 预期收益

- 📈 对话连贯性：**+30-50%**
- 😊 用户满意度：**+20-35%**
- 🔄 重复问题：**-40-60%**
- ⏱️ 平均处理时间：**-25-40%**

---

## 🛠️ 实施方案

### Python 环境 (技术团队)

**推荐技术栈**:
```
Mem0 (记忆层) + Qdrant (向量库) + SQLite (结构化) + LangChain (编排)
```

**核心代码**:
```python
from mem0 import Memory

memory = Memory(
    vector_store={"provider": "qdrant", "config": {"url": "http://localhost:6333"}},
    embedder={"provider": "huggingface", "config": {"model": "BAAI/bge-m3"}},
    llm={"provider": "ollama", "config": {"model": "llama3.1:8b"}}
)

# 添加记忆
memory.add("用户喜欢冰美式咖啡", user_id="user_123")

# 检索记忆
results = memory.search("咖啡偏好", user_id="user_123")
```

👉 详细文档：[docs/04-落地实施方案/01-Python 环境实施方案.md](docs/04-落地实施方案/01-Python 环境实施方案.md)

### Dify 工作流 (产品团队)

**推荐方案**:
```
Dify 长期记忆插件 + 知识库 + 工作流变量
```

**核心配置**:
1. 启用 Dify 长期记忆功能
2. 配置知识库向量检索
3. 在工作流中添加记忆读写节点

👉 详细文档：[docs/04-落地实施方案/02-Dify 工作流实施方案.md](docs/04-落地实施方案/02-Dify 工作流实施方案.md)

---

## 🔄 自动化更新

本项目每两天自动更新最新研究资料。

### 设置更新

```bash
# 进入项目目录
cd long-term-memory-research

# 测试运行
./scripts/update.sh --dry-run

# 设置定时任务 (每两天凌晨 2 点)
./scripts/update.sh --setup-cron

# 手动更新
./scripts/update.sh --force
```

### 更新内容

- 📚 学术论文 (arXiv、学术会议)
- 🔧 开源项目 (GitHub Release)
- 🏢 工业案例 (企业实践)
- 📊 性能基准

### 更新日志

查看 `.update_log.md` 了解最新变更。

---

## 📚 文档导航

### 入门指南
- [执行摘要](docs/00-执行摘要.md) - 5 分钟快速了解
- [方案选型决策树](docs/04-落地实施方案/03-方案选型决策树.md) - 选择适合的方案

### 技术深入
- [向量记忆技术](docs/01-技术方向/01-向量记忆技术.md) - 最成熟的方案
- [图结构记忆](docs/01-技术方向/02-图结构记忆.md) - 关系推理
- [分层记忆架构](docs/01-技术方向/03-分层记忆架构.md) - 核心/归档/对话

### 应用场景
- [客户服务](docs/02-应用场景/01-客户服务场景.md) - Zendesk 案例
- [个人助理](docs/02-应用场景/02-个人助理场景.md) - 轻量级方案
- [教育](docs/02-应用场景/03-教育场景.md) - 可汗学院案例
- [医疗健康](docs/02-应用场景/04-医疗健康场景.md) - HIPAA 合规
- [企业知识管理](docs/02-应用场景/05-企业知识管理.md) - 咨询公司案例

### 行业调研
- [学术研究前沿](docs/03-全网资料深度探索/01-学术研究前沿.md) - 2024-2025 论文
- [工业界落地案例](docs/03-全网资料深度探索/02-工业界落地案例.md) - 7 个企业案例
- [开源项目对比](docs/03-全网资料深度探索/03-开源项目对比.md) - 工具选型
- [安全与治理](docs/03-全网资料深度探索/04-安全与治理.md) - 隐私/合规

### 实施指南
- [Python 方案](docs/04-落地实施方案/01-Python 环境实施方案.md) - 完整代码
- [Dify 方案](docs/04-落地实施方案/02-Dify 工作流实施方案.md) - 低代码
- [关键术语表](docs/05-附录/01-关键术语表.md) - 50+ 术语解释

---

## 🏆 工业案例

### 客户服务 - Zendesk + Mem0

| 指标 | 改善 |
|------|------|
| 客户满意度 (CSAT) | +18% |
| 首次响应解决率 | +23% |
| 平均处理时间 | -31% |
| 客户重复问题 | -45% |

### 个人助理 - Replit Agent

| 指标 | 改善 |
|------|------|
| 代码建议准确率 | +34% |
| 用户留存率 | +27% |
| 付费转化率 | +19% |

### 教育 - Khanmigo (可汗学院)

| 指标 | 改善 |
|------|------|
| 学生学习时长 | +42% |
| 知识点掌握速度 | +28% |
| 学习满意度 | +35% |

👉 更多案例：[docs/03-全网资料深度探索/02-工业界落地案例.md](docs/03-全网资料深度探索/02-工业界落地案例.md)

---

## 🤝 贡献指南

欢迎贡献！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 贡献方式

1. 📝 补充新论文/案例
2. 🐛 修正错误
3. 💡 改进建议
4. 🔧 完善代码示例
5. 🌍 翻译文档

### 提交流程

```bash
# 1. Fork 项目
# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交更改
git commit -m "Add: your feature"

# 4. 推送分支
git push origin feature/your-feature

# 5. 创建 Pull Request
```

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## 📬 联系方式

- 📧 Issues: [GitHub Issues](https://github.com/yrju/long-term-memory-research/issues)
- 💬 讨论：[GitHub Discussions](https://github.com/yrju/long-term-memory-research/discussions)
- 📧 Email: [通过 GitHub 联系](https://github.com/yrju)

---

## 🙏 致谢

感谢以下开源项目：

- [Mem0](https://github.com/mem0ai/mem0) - 通用记忆层
- [Letta](https://github.com/cpacker/Letta) - 分层记忆
- [LangChain](https://github.com/langchain-ai/langchain) - LLM 编排
- [Qdrant](https://github.com/qdrant/qdrant) - 向量数据库
- [Dify](https://github.com/langgenius/dify) - 低代码平台

---

## 📈 项目统计

![Stars](https://img.shields.io/github/stars/yrju/long-term-memory-research?style=social)
![Forks](https://img.shields.io/github/forks/yrju/long-term-memory-research?style=social)
![Issues](https://img.shields.io/github/issues/yrju/long-term-memory-research)
![Last Commit](https://img.shields.io/github/last-commit/yrju/long-term-memory-research)

---

**📅 最后更新**: 2026-03-14  
**🔄 下次自动更新**: 2026-03-16  
**⭐ 如果这个项目对你有帮助，请给一个 Star!**
