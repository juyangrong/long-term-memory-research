# DeepAnalyze 技能

## 描述

数据分析任务专用技能。当用户请求涉及**数据分析**、**数据报告**、**趋势分析**、**风险洞察**等任务时，自动使用 DeepAnalyze-8B 模型配合 DeepAnalyze 工程化代码执行分析。

## 触发条件

激活当用户消息包含以下关键词或意图：
- 数据分析
- 数据报告
- 趋势分析
- 风险洞察
- 深度分析
- 数据洞察
- 统计分析
- 数据可视化

## 模型配置

- **模型**: `DeepAnalyze-8B` (alias: `custom-aigw-fx-ctripcorp-com-3/DeepAnalyze-8B`)
- **API URL**: `http://aigw.fx.ctripcorp.com/llm/100000872/v1`
- **API Key**: `sk-4b07a192-1a1c-4e28-83c5-ac7123b49691`

## 工程代码路径

DeepAnalyze 工程代码位于：
```
/home/rskuser/.openclaw/workspace/DeepAnalyze/
```

核心文件：
- `deepanalyze.py` - 主分析引擎
- `deepanalyze/` - 核心模块目录
- `risk_analysis.py` - 风险分析脚本
- `client.py` - API 客户端

## 使用方式

### 1. 模型调用

在子代理或任务执行时，指定模型为 `DeepAnalyze-8B`：

```bash
# 使用模型别名
openclaw run --model DeepAnalyze-8B "分析机票风险趋势"
```

### 2. 代码集成

分析任务可直接调用 DeepAnalyze 工程代码：

```python
import sys
sys.path.insert(0, '/home/rskuser/.openclaw/workspace/DeepAnalyze')
from deepanalyze import analyze

result = analyze(data, task="风险趋势分析")
```

### 3. 子代理执行

对于复杂分析任务， spawn 子代理使用 DeepAnalyze-8B：

```
sessions_spawn(
  task="使用 DeepAnalyze 代码分析机票风险数据",
  model="DeepAnalyze-8B",
  runtime="subagent"
)
```

## 注意事项

1. **仅用于数据分析任务** - 不要将 DeepAnalyze-8B 用于通用对话或其他任务
2. **工程代码优先** - 分析任务应优先使用 DeepAnalyze 工程化代码，而非从头实现
3. **模型上下文** - DeepAnalyze-8B 的 contextWindow 为 128k，适合处理大规模数据

## 测试

测试连接：
```bash
cd /home/rskuser/.openclaw/workspace/DeepAnalyze
python test_connection.py
```
