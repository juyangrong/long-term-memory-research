# Dify 工作流示例

本目录包含 Dify 平台的长期记忆工作流配置示例。

## 文件说明

| 文件 | 功能 |
|------|------|
| `memory_workflow.json` | 基础记忆工作流 |
| `advanced_workflow.json` | 进阶记忆工作流 (含 HTTP 请求) |

## 导入工作流

### 步骤 1: 登录 Dify

访问 [Dify Cloud](https://cloud.dify.ai) 或你的自托管实例。

### 步骤 2: 创建工作流应用

1. 进入「工作室」
2. 点击「创建应用」
3. 选择「工作流」类型
4. 命名应用 (如「长期记忆助手」)

### 步骤 3: 导入配置

1. 在工作流编辑页面，点击右上角「...」
2. 选择「导入 DSL」
3. 上传 `memory_workflow.json` 文件
4. 确认导入

### 步骤 4: 配置参数

根据实际需求调整:

- **知识库**: 选择或创建你的记忆知识库
- **LLM 模型**: 选择你的模型 (GPT-4/Claude/本地)
- **变量**: 配置用户画像等变量

### 步骤 5: 测试运行

1. 点击「运行」
2. 输入测试消息
3. 查看输出结果

## 工作流说明

### 基础工作流 (memory_workflow.json)

```
开始 → 知识库检索 → LLM 生成 → 结束
```

适合快速原型验证。

### 进阶工作流 (advanced_workflow.json)

```
开始 → 意图识别 → 
  ├─ 需要记忆 → HTTP 请求 (检索) → LLM 生成 → HTTP 请求 (更新) → 结束
  └─ 无需记忆 → LLM 生成 → 结束
```

适合生产环境，支持外部记忆服务。

## 配置外部记忆服务

如需使用外部记忆服务 (Python API):

### 1. 部署记忆服务

参考 [Python 示例](../python/) 部署记忆 API。

### 2. 配置 HTTP 请求节点

在工作流中添加 HTTP 请求节点:

```yaml
URL: http://your-api.com/memories/search
Method: POST
Headers:
  Content-Type: application/json
Body:
  user_id: {{user.id}}
  query: {{message}}
  limit: 5
```

### 3. 解析响应

使用代码节点解析 HTTP 响应:

```python
def main(response):
    memories = response.get('results', [])
    return {'memories': memories}
```

## 详细文档

完整实施指南见：[docs/04-落地实施方案/02-Dify 工作流实施方案.md](../docs/04-落地实施方案/02-Dify 工作流实施方案.md)

## 故障排查

### 问题 1: 导入失败

**原因**: Dify 版本过低  
**解决**: 升级到 0.6.0+ 版本

### 问题 2: 知识库检索为空

**原因**: 知识库无数据  
**解决**: 先向知识库添加文档

### 问题 3: HTTP 请求失败

**原因**: 网络不通或 API 错误  
**解决**: 检查 API 地址和认证

---

需要帮助？查看 [Dify 官方文档](https://docs.dify.ai/)
