# DeepAnalyze 配置记录

**配置日期**: 2026-03-19

## 模型信息

| 配置项 | 值 |
|--------|-----|
| 模型名称 | DeepAnalyze-8B |
| Provider | custom-aigw-fx-ctripcorp-com-3 |
| API URL | http://aigw.fx.ctripcorp.com/llm/100000872/v1 |
| API Key | sk-4b07a192-1a1c-4e28-83c5-ac7123b49691 |
| Context Window | 128000 |
| Max Tokens | 32000 |

## 路由规则

**当任务涉及以下内容时，使用 DeepAnalyze-8B 模型**：
- 数据分析
- 数据报告
- 趋势分析
- 风险洞察
- 深度分析
- 数据洞察
- 统计分析
- 数据可视化

## 工程代码位置

```
/home/rskuser/.openclaw/workspace/DeepAnalyze/
```

## 使用方式

1. **模型调用**: 使用别名 `DeepAnalyze-8B` 或完整路径 `custom-aigw-fx-ctripcorp-com-3/DeepAnalyze-8B`
2. **代码集成**: 直接调用 DeepAnalyze 工程代码
3. **子代理**: spawn 子代理时指定 `model="DeepAnalyze-8B"`

## 测试状态

- [x] 模型连接测试 - 2026-03-19 测试通过
- [x] 核心依赖安装 - openai, pandas, numpy, matplotlib, seaborn, scikit-learn
- [ ] 路由规则测试

## 安装说明

由于磁盘空间限制（/ 只有 25G），仅安装了核心依赖：
- openai (API 调用)
- pandas, numpy (数据处理)
- matplotlib, seaborn (可视化)
- scikit-learn (机器学习)

未安装的大型包：vllm, torch, transformers (需要 ~10G+ 空间)
