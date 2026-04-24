# Harness 技术方案调研报告

> 调研日期：2026 年 3 月 31 日  
> 调研范围：基于 Harness 的 AI Agent 开发框架与技术解决方案

---

## 目录

1. [Embabel - AI Agent 开发框架](#1-embabel---ai-agent-开发框架)
2. [AgentScope Java - 多智能体协作框架](#2-agentscope-java---多智能体协作框架)
3. [Spring AI - Spring 生态的 AI 集成框架](#3-spring-ai---spring-生态的 ai 集成框架)
4. [LangChain4J - Java 版 LangChain](#4-langchain4j---java-版-langchain)
5. [Semantic Kernel - 微软 AI SDK](#5-semantic-kernel---微软 ai-sdk)
6. [方案对比总结](#6-方案对比总结)
7. [选型建议](#7-选型建议)

---

## 1. Embabel - AI Agent 开发框架

### 1.1 项目信息

| 项目 | 信息 |
|------|------|
| **GitHub 仓库** | https://github.com/embabel/embabel-agent |
| **文档站点** | https://docs.embabel.com/embabel-agent/guide/0.1.2-SNAPSHOT/ |
| **最新版本** | 0.1.2-SNAPSHOT (2025 年 2 月) |
| **许可证** | Apache 2.0 |
| **语言支持** | Kotlin, Java (JVM 平台) |
| **社区** | Discord: https://discord.gg/t6bjkyj93q |

### 1.2 核心架构和工作原理

Embabel 是一个为 JVM 设计的智能体框架，发音为 Em-BAY-bel (/ɛmˈbeɪbəl/)。其核心理念是提供**代码代理**和**LLM 代理**的结合。

#### 架构特点

```
┌─────────────────────────────────────────────────────────┐
│                    Embabel Platform                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Planning   │  │   Domain    │  │   LLM Mixing    │  │
│  │   Engine    │  │   Model     │  │   (Multi-model) │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Actions   │  │    Goals    │  │   Conditions    │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### 核心概念

- **Domain Model**: 强类型领域模型，包含行为和条件
- **Actions**: 可执行的操作，由 LLM 或代码实现
- **Goals**: 目标定义，驱动规划引擎
- **Conditions**: 执行条件，控制流程
- **Planning Engine**: 非 LLM AI 算法进行任务规划

### 1.3 主要功能和特性

| 功能 | 描述 |
|------|------|
| **Sophisticated Planning** | 超越有限状态机的真正规划步骤，支持并行化决策 |
| **Superior Extensibility** | 通过添加领域对象、动作、目标扩展能力，无需修改现有代码 |
| **Strong Typing** | 强类型和面向对象设计，支持完整重构 |
| **Platform Abstraction** | 编程模型与平台内部 cleanly 分离 |
| **LLM Mixing** | 支持混合使用不同 LLM，优化成本和性能 |
| **GuardRails** | 实验性集成 OpenAI SDK GuardRails |
| **Observability** | 内置可观测性支持 (embabel-agent-observability) |

### 1.4 适用场景和局限性

#### 适用场景
- ✅ 需要可解释性的业务应用
- ✅ 复杂任务分解和规划
- ✅ 多模型混合使用场景
- ✅ 需要强类型安全的 Java/Kotlin 项目
- ✅ 企业级 Agent 联邦系统

#### 局限性
- ⚠️ 相对较新，社区规模较小
- ⚠️ 文档仍在完善中
- ⚠️ 主要面向 JVM 生态

### 1.5 社区活跃度和生态

- **GitHub Stars**: 持续增长中
- **发布频率**: 活跃开发，2025 年 2 月有重要更新
- **集成**: Spring Boot, Kotlin, Maven, JUnit5
- **模型支持**: ChatGPT, Jinja, JSON 等

---

## 2. AgentScope Java - 多智能体协作框架

### 2.1 项目信息

| 项目 | 信息 |
|------|------|
| **GitHub 仓库** | https://github.com/agentscope-ai/agentscope-java |
| **文档站点** | https://java.agentscope.io/ |
| **最新版本** | 1.0.10 (2026 年 3 月) |
| **许可证** | Apache 2.0 |
| **语言支持** | Java 17+ |
| **社区** | Discord: https://discord.gg/eYMpfnkG8h |

### 2.2 核心架构和工作原理

AgentScope Java 是阿里巴巴推出的面向智能体的编程框架，基于 **Project Reactor** 构建响应式、非阻塞执行架构。

#### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                  AgentScope Java                          │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ ReAct Agent  │  │ Tool Calling │  │ Memory Mgmt   │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Multi-Agent  │  │  MCP Protocol│  │  A2A Protocol │  │
│  │ Collaboration│  │  Integration │  │  (Nacos)      │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Runtime    │  │    Studio    │  │ Observability │  │
│  │  (Sandbox)   │  │  (Visual)    │  │  (OpenTelemetry)│ │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 2.3 主要功能和特性

| 功能 | 描述 |
|------|------|
| **ReAct Reasoning** | 自主规划和执行复杂任务，动态决定工具使用 |
| **Safe Interruption** | 安全中断 Agent 执行，保留完整上下文和工具状态 |
| **Graceful Cancellation** | 优雅取消长时间运行的工具调用 |
| **Human-in-the-Loop** | 通过 Hook 系统注入人工干预 |
| **PlanNotebook** | 结构化任务管理系统，分解复杂目标 |
| **Structured Output** | 自校正输出解析器，保证类型安全响应 |
| **Long-term Memory** | 持久化存储，支持语义搜索和多租户隔离 |
| **RAG Integration** | 与企业知识库无缝集成 |
| **MCP Protocol** | 集成任何 MCP 兼容服务器 |
| **A2A Protocol** | 通过 Nacos 实现分布式多 Agent 协作 |
| **GraalVM Native** | 200ms 冷启动时间，适合 Serverless |

### 2.4 适用场景和局限性

#### 适用场景
- ✅ 企业级多 Agent 协作系统
- ✅ 需要高并发和响应式架构的场景
- ✅ 生产环境部署 (沙箱隔离)
- ✅ 需要可视化开发和监控
- ✅ 微服务架构集成

#### 局限性
- ⚠️ 需要 Java 17+ 环境
- ⚠️ 学习曲线较陡 (响应式编程)
- ⚠️ 主要面向企业级应用

### 2.5 社区活跃度和生态

- **最新版本**: 1.0.10 (2026 年 3 月 11 日发布)
- **发布频率**: 高度活跃，持续更新
- **生态系统**: 
  - AgentScope Runtime (沙箱执行)
  - AgentScope Studio (可视化开发)
  - 与阿里云百炼集成
- **社区**: Discord 活跃，中文文档完善

---

## 3. Spring AI - Spring 生态的 AI 集成框架

### 3.1 项目信息

| 项目 | 信息 |
|------|------|
| **GitHub 仓库** | https://github.com/spring-projects/spring-ai |
| **文档站点** | https://docs.spring.io/spring-ai/reference/ |
| **最新版本** | 2.0.0-M4 (2026 年 3 月) |
| **许可证** | Apache 2.0 |
| **语言支持** | Java 17+ (Spring Boot 4.x) |
| **官方支持** | VMware/Spring 团队 |

### 3.2 核心架构和工作原理

Spring AI 是 Spring 官方推出的 AI 应用框架，将 Spring 生态系统设计原则应用于 AI 领域。

#### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                     Spring AI                             │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  ChatClient  │  │  ChatModel   │  │   Advisors    │  │
│  │    (API)     │  │  (Provider)  │  │   (Patterns)  │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │    Tools     │  │   Vector     │  │  Observability│  │
│  │  (Function)  │  │   Stores     │  │  (OpenTelemetry)│ │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │     RAG      │  │     ETL      │  │   Evaluation  │  │
│  │  (Retrieval) │  │  (Document)  │  │   (Testing)   │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 3.3 主要功能和特性

| 功能 | 描述 |
|------|------|
| **多模型支持** | OpenAI, Anthropic, Azure, Google, Amazon, Ollama 等 20+ 提供商 |
| **模型类型** | Chat Completion, Embedding, Text-to-Image, Audio, Moderation |
| **Vector Stores** | 30+ 向量数据库支持 (PGVector, Pinecone, Redis, Milvus 等) |
| **Tools/Function Calling** | 支持模型调用客户端工具和方法 |
| **Structured Outputs** | AI 输出映射到 POJO |
| **ChatClient API** | 类似 WebClient 的流畅 API |
| **Advisors API** | 封装生成式 AI 模式 |
| **Chat Memory** | 对话记忆支持 |
| **RAG** | 检索增强生成 |
| **ETL Pipeline** | 文档注入数据处理 |
| **Model Evaluation** | 评估生成内容，防止幻觉 |
| **Spring Boot AutoConfig** | 开箱即用的 Starter |

### 3.4 适用场景和局限性

#### 适用场景
- ✅ Spring Boot 项目集成 AI 能力
- ✅ 企业级 AI 应用开发
- ✅ 需要多模型供应商支持
- ✅ RAG 和文档问答系统
- ✅ 需要稳定 API 和长期支持

#### 局限性
- ⚠️ 相比 LangChain 功能较为基础
- ⚠️ Agent 编排能力相对简单
- ⚠️ 部分高级功能仍在开发中

### 3.5 社区活跃度和生态

- **最新版本**: 2.0.0-M4 (2026 年 3 月 26 日发布)
- **发布频率**: 高度活跃，Spring 官方支持
- **生态系统**: 
  - 完整的 Spring 生态集成
  - start.spring.io 一键创建
  - 企业级支持
- **社区**: 庞大 Spring 社区支持，文档完善

---

## 4. LangChain4J - Java 版 LangChain

### 4.1 项目信息

| 项目 | 信息 |
|------|------|
| **GitHub 仓库** | https://github.com/langchain4j/langchain4j |
| **文档站点** | https://docs.langchain4j.dev/ |
| **最新版本** | 持续更新 (Maven Central) |
| **许可证** | Apache 2.0 |
| **语言支持** | Java 8+ |
| **社区** | Discord: https://discord.gg/JzTFvyjG6R |

### 4.2 核心架构和工作原理

LangChain4J 是 LangChain 的 Java 版本，但不仅仅是移植，而是融合了 LangChain、Haystack、LlamaIndex 等项目的理念和最佳实践。

#### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                    LangChain4J                            │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  LLM         │  │   Embedding  │  │   Vector      │  │
│  │  Providers   │  │   Models     │  │   Stores      │  │
│  │  (20+)       │  │              │  │   (30+)       │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Prompt     │  │  Chat Memory │  │  Tool Calling │  │
│  │  Templating  │  │  Management  │  │  (MCP)        │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │    Agents    │  │     RAG      │  │  Integrations │  │
│  │  (Patterns)  │  │  (Pipeline)  │  │  (Quarkus,    │  │
│  │              │  │              │  │   Spring)     │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 4.3 主要功能和特性

| 功能 | 描述 |
|------|------|
| **统一 API** | 20+ LLM 提供商，30+ 向量数据库的统一接口 |
| **Prompt Templating** | 低级别提示词模板 |
| **Chat Memory** | 对话记忆管理 |
| **Function Calling** | 工具调用 (支持 MCP) |
| **Agents** | 高级 Agent 模式 |
| **RAG** | 完整的 RAG 流程 (从数据摄入到检索) |
| **框架集成** | Quarkus, Spring Boot, Helidon |
| **丰富示例** | 大量示例代码 (langchain4j-examples) |
| **双向集成** | Java 调用 LLM + LLM 调用 Java 代码 |

### 4.4 适用场景和局限性

#### 适用场景
- ✅ 快速原型开发和实验
- ✅ 需要丰富 LLM 和向量数据库支持
- ✅ RAG 应用开发
- ✅ Quarkus/Spring Boot 项目
- ✅ 需要大量现成示例和模板

#### 局限性
- ⚠️ 功能迭代快速，API 可能变化
- ⚠️ 相比 Python LangChain 功能仍有差距
- ⚠️ 企业级特性相对较少

### 4.5 社区活跃度和生态

- **发布频率**: 高度活跃
- **生态系统**: 
  - langchain4j-examples 仓库
  - Quarkus 集成
  - Spring Boot 集成
  - 文档聊天机器人 (experimental)
- **社区**: Discord 活跃，Twitter/X 有官方账号

---

## 5. Semantic Kernel - 微软 AI SDK

### 5.1 项目信息

| 项目 | 信息 |
|------|------|
| **GitHub 仓库** | https://github.com/microsoft/semantic-kernel (多语言)<br>https://github.com/microsoft/semantic-kernel-java (Java 专用) |
| **文档站点** | https://learn.microsoft.com/en-us/semantic-kernel/ |
| **最新版本** | 1.0+ (稳定版本) |
| **许可证** | MIT |
| **语言支持** | Java 17+, Python 3.10+, .NET 10.0+ |
| **官方支持** | Microsoft |

### 5.2 核心架构和工作原理

Semantic Kernel 是微软推出的轻量级开源开发工具包，支持 C#、Python 和 Java。

#### 架构设计

```
┌──────────────────────────────────────────────────────────┐
│                  Semantic Kernel                          │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │    Agent     │  │   Plugins    │  │   Planner     │  │
│  │   Framework  │  │  (Functions) │  │   (AI)        │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Multi-Agent │  │   Memory     │  │  Observability│  │
│  │   Systems    │  │   (Vector)   │  │  (Telemetry)  │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │     MCP      │  │   Process    │  │   Multimodal  │  │
│  │  Protocol    │  │   Framework  │  │   Support     │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 5.3 主要功能和特性

| 功能 | 描述 |
|------|------|
| **多语言支持** | Java, Python, .NET 统一 API |
| **模型灵活性** | OpenAI, Azure OpenAI, Hugging Face, NVIDIA, Ollama, LMStudio |
| **Agent Framework** | 模块化 AI Agent，支持工具/插件、记忆、规划 |
| **Multi-Agent Systems** | 协作式专家 Agent 系统 |
| **Plugin Ecosystem** | 本地代码函数、提示模板、OpenAPI、MCP |
| **Vector DB** | Azure AI Search, Elasticsearch, Chroma 等 |
| **Multimodal** | 文本、视觉、音频输入 |
| **Process Framework** | 结构化业务流程建模 |
| **Enterprise Ready** | 可观测性、安全性、稳定 API |
| **版本 1.0+** | 跨语言稳定版本，承诺非破坏性变更 |

### 5.4 适用场景和局限性

#### 适用场景
- ✅ 微软技术栈企业 (Azure, .NET)
- ✅ 需要多语言统一 API
- ✅ 企业级 AI 应用
- ✅ 复杂业务流程建模
- ✅ 需要官方长期支持

#### 局限性
- ⚠️ Java 版本相对 C#/Python 较新
- ⚠️ 部分高级功能 Java 支持有限
- ⚠️ 主要面向微软生态

### 5.5 社区活跃度和生态

- **发布频率**: 活跃，微软官方支持
- **生态系统**: 
  - Azure 深度集成
  - 多语言统一 SDK
  - 企业级支持
- **社区**: Discord 活跃，Microsoft Learn 文档完善

---

## 6. 方案对比总结

### 6.1 功能对比表

| 特性 | Embabel | AgentScope Java | Spring AI | LangChain4J | Semantic Kernel |
|------|---------|-----------------|-----------|-------------|-----------------|
| **核心定位** | JVM 智能体平台 | 企业级多 Agent | Spring AI 集成 | Java LangChain | 微软 AI SDK |
| **语言** | Kotlin/Java | Java 17+ | Java 17+ | Java 8+ | Java 17+/Python/.NET |
| **最新版本** | 0.1.2-SNAPSHOT | 1.0.10 | 2.0.0-M4 | 持续更新 | 1.0+ |
| **规划引擎** | ✅ 非 LLM AI 规划 | ✅ ReAct | ⚠️ 基础 | ✅ Agent 模式 | ✅ AI Planner |
| **多 Agent** | ⚠️ 联邦支持 | ✅ 完整支持 | ⚠️ 基础 | ✅ 支持 | ✅ 完整系统 |
| **MCP 协议** | ✅ 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| **RAG** | ✅ 支持 | ✅ 支持 | ✅ 完整 | ✅ 完整 | ✅ 支持 |
| **向量数据库** | ⚠️ 有限 | ✅ 多支持 | ✅ 30+ | ✅ 30+ | ✅ 多支持 |
| **LLM 提供商** | ✅ 多模型 | ✅ 多模型 | ✅ 20+ | ✅ 20+ | ✅ 多模型 |
| **可视化** | ❌ | ✅ Studio | ❌ | ❌ | ⚠️ 有限 |
| **沙箱隔离** | ✅ Runtime | ✅ Runtime | ❌ | ❌ | ⚠️ 有限 |
| **响应式** | ❌ | ✅ Project Reactor | ⚠️ 可选 | ❌ | ❌ |
| **原生编译** | ❌ | ✅ GraalVM | ⚠️ 支持 | ❌ | ❌ |
| **官方支持** | 社区 | 阿里巴巴 | Spring 官方 | 社区 | 微软 |

### 6.2 社区活跃度对比

| 指标 | Embabel | AgentScope Java | Spring AI | LangChain4J | Semantic Kernel |
|------|---------|-----------------|-----------|-------------|-----------------|
| **GitHub Stars** | 增长中 | 高 | 非常高 | 非常高 | 非常高 |
| **发布频率** | 活跃 | 非常活跃 | 非常活跃 | 非常活跃 | 活跃 |
| **文档质量** | 良好 | 优秀 | 优秀 | 优秀 | 优秀 |
| **社区支持** | Discord | Discord | 庞大 Spring 社区 | Discord/Twitter | Discord/MS Learn |
| **企业采用** | 早期 | 阿里巴巴生态 | 广泛 | 增长中 | 微软及合作伙伴 |

### 6.3 优缺点总结

#### Embabel
**优点:**
- ✅ 独特的非 LLM AI 规划引擎
- ✅ 强类型和面向对象设计
- ✅ LLM 混合使用优化
- ✅ 可解释性强

**缺点:**
- ⚠️ 相对较新，社区较小
- ⚠️ 文档仍在完善

#### AgentScope Java
**优点:**
- ✅ 企业级功能完整
- ✅ 响应式高并发架构
- ✅ 可视化工具 (Studio)
- ✅ 沙箱隔离生产就绪
- ✅ 阿里巴巴背书

**缺点:**
- ⚠️ Java 17+ 要求
- ⚠️ 响应式编程学习曲线

#### Spring AI
**优点:**
- ✅ Spring 官方支持
- ✅ 完整 Spring 生态集成
- ✅ 稳定 API 承诺
- ✅ 企业级支持
- ✅ 丰富的向量数据库支持

**缺点:**
- ⚠️ Agent 编排相对简单
- ⚠️ 部分高级功能开发中

#### LangChain4J
**优点:**
- ✅ 丰富的 LLM 和向量库支持
- ✅ 大量示例代码
- ✅ 快速原型开发
- ✅ 框架集成良好

**缺点:**
- ⚠️ API 变化较快
- ⚠️ 企业级特性较少

#### Semantic Kernel
**优点:**
- ✅ 微软官方支持
- ✅ 多语言统一 API
- ✅ 企业级特性完整
- ✅ 稳定版本 1.0+
- ✅ Azure 深度集成

**缺点:**
- ⚠️ Java 版本相对较新
- ⚠️ 主要面向微软生态

---

## 7. 选型建议

### 7.1 按场景推荐

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| **Spring Boot 项目** | Spring AI | 原生集成，生态完整 |
| **企业级多 Agent** | AgentScope Java | 生产就绪，功能完整 |
| **快速原型** | LangChain4J | 示例丰富，上手快 |
| **微软技术栈** | Semantic Kernel | Azure 集成，官方支持 |
| **复杂规划场景** | Embabel | 独特规划引擎 |
| **需要可视化** | AgentScope Java | Studio 工具 |
| **多语言统一** | Semantic Kernel | Java/Python/.NET统一API |
| **响应式高并发** | AgentScope Java | Project Reactor 架构 |

### 7.2 综合推荐

**企业级生产环境首选:**
1. **AgentScope Java** - 功能最完整，生产就绪
2. **Spring AI** - Spring 生态最佳选择
3. **Semantic Kernel** - 微软技术栈首选

**快速开发和原型:**
1. **LangChain4J** - 示例丰富，快速上手
2. **Spring AI** - 如果已有 Spring Boot 项目

**创新和实验性项目:**
1. **Embabel** - 独特规划能力
2. **AgentScope Java** - 最新特性支持

### 7.3 技术趋势观察

1. **MCP 协议标准化**: 所有主流框架都在集成 MCP (Model Context Protocol)
2. **多 Agent 协作**: 从单 Agent 向多 Agent 系统演进
3. **企业级特性**: 可观测性、沙箱隔离、原生编译成为标配
4. **可视化开发**: AgentScope Studio 引领可视化趋势
5. **响应式架构**: 高并发场景推动响应式编程采用

---

## 附录：快速开始参考

### Embabel
```kotlin
// Maven 依赖
implementation("com.embabel:embabel-agent-api:0.1.2-SNAPSHOT")
```

### AgentScope Java
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>io.agentscope</groupId>
    <artifactId>agentscope-java</artifactId>
    <version>1.0.10</version>
</dependency>
```

### Spring AI
```xml
<!-- Maven 依赖 (Spring Boot 4.x) -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
    <version>2.0.0-M4</version>
</dependency>
```

### LangChain4J
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j</artifactId>
    <version>latest</version>
</dependency>
```

### Semantic Kernel
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>com.microsoft.semantic-kernel</groupId>
    <artifactId>semantickernel-api</artifactId>
    <version>1.0+</version>
</dependency>
```

---

> **报告生成时间**: 2026 年 3 月 31 日  
> **调研方法**: 官方文档、GitHub 仓库、技术博客、社区讨论  
> **免责声明**: 信息可能随时变化，请以官方最新文档为准
