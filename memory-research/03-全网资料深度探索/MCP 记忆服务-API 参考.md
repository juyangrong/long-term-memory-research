# MCP 记忆服务 API 参考

**服务名称**: 智能体记忆层 MCP 服务  
**API 端点**: `http://aigw.fx.ctripcorp.com/mcp/100000013/mcp`  
**协议**: MCP + Streamable HTTP  
**最后更新**: 2026-03-22

---

## 📋 概述

智能体记忆层 MCP 服务提供用户长期记忆的存储和检索能力，支持跨应用共享用户画像和偏好信息。

### 核心能力

- ✅ 用户偏好记忆存储
- ✅ 语义检索相关记忆
- ✅ 记忆增删改查 (CRUD)
- ✅ 元数据分类过滤
- ✅ 多用户支持
- ✅ Streamable HTTP 协议

---

## 🔑 认证参数

所有 API 支持以下身份参数（可选，为空时从 headers/query 自动获取）：

| 参数 | 说明 | 来源优先级 |
|------|------|-----------|
| `user_id` | 用户身份 id | 参数 > headers > query_param |
| `run_id` | 会话 id | 参数 > headers > query_param |
| `agent_id` | 应用 id | 参数 > headers > query_param |

---

## 📖 API 列表

| API | 功能 | 必填参数 |
|-----|------|----------|
| [`add_memory`](#add_memory) | 添加用户记忆 | `content` |
| [`search_memory`](#search_memory) | 检索记忆 | `content` |
| [`update_memory`](#update_memory) | 更新记忆 | `memory_id`, `content` |
| [`get_memory`](#get_memory) | 获取单条记忆 | `memory_id` |
| [`get_all_memory`](#get_all_memory) | 获取所有记忆 | - |
| [`delete_memory`](#delete_memory) | 删除记忆 | `memory_id` |

---

## API 详解

### add_memory

**功能**: 从用户指令中识别偏好，保存到记忆服务

**参数**:
```json
{
  "method": "add_memory",
  "params": {
    "content": "string (必填) - 用户输入的原始消息内容",
    "user_id": "string (可选) - 用户身份 id",
    "run_id": "string (可选) - 会话 id",
    "agent_id": "string (可选) - 应用 id",
    "metadata": "string (可选) - JSON 对象字符串，记忆数据的属性特征"
  }
}
```

**metadata 格式示例**:

```json
// 爱好分类
{"category":"hobbies"}

// Coding 工程信息
{
  "project":"my_project",
  "language":"python",
  "framework":"flask",
  "database":"mysql",
  "cloud_service":"aliyun"
}

// 未来计划行为
{
  "plan":"travel_to_shanghai",
  "date":"2025-12-05",
  "destination":"shanghai"
}

// 重要个人信息
{
  "name":"张三",
  "age":"20",
  "gender":"male",
  "email":"zhangsan@example.com",
  "phone":"12345678901"
}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "add_memory",
    "params": {
      "content": "用户喜欢冰美式咖啡",
      "user_id": "employee_123",
      "metadata": "{\"category\":\"hobbies\",\"type\":\"beverage\"}"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memory_id": "mem_abc123",
  "message": "记忆添加成功"
}
```

---

### search_memory

**功能**: 按用户输入内容检索最相关的记忆数据

**参数**:
```json
{
  "method": "search_memory",
  "params": {
    "content": "string (必填) - 用户输入的原始消息内容",
    "user_id": "string (可选) - 用户身份 id",
    "run_id": "string (可选) - 会话 id",
    "agent_id": "string (可选) - 应用 id",
    "limit": "string (可选) - 返回条数，默认 100",
    "filters": "string (可选) - JSON 对象字符串，过滤条件"
  }
}
```

**filters 格式示例**:

```json
// 工作场景
{"scene":"work"}

// 特定项目
{"project":"my_project"}

// 计划行为
{"plan":"travel_to_shanghai"}

// 个人信息
{"name":"张三"}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "search_memory",
    "params": {
      "content": "咖啡",
      "user_id": "employee_123",
      "limit": "10",
      "filters": "{\"category\":\"hobbies\"}"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memories": [
    {
      "memory_id": "mem_abc123",
      "content": "用户喜欢冰美式咖啡",
      "metadata": {"category":"hobbies","type":"beverage"},
      "score": 0.95,
      "created_at": "2026-03-22T10:00:00Z"
    }
  ]
}
```

---

### update_memory

**功能**: 根据 memory_id 更新指定记忆内容

**参数**:
```json
{
  "method": "update_memory",
  "params": {
    "memory_id": "string (必填) - 记忆数据 ID",
    "content": "string (必填) - 新的偏好内容文本"
  }
}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "update_memory",
    "params": {
      "memory_id": "mem_abc123",
      "content": "用户喜欢热拿铁咖啡 (更新)"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memory_id": "mem_abc123",
  "message": "记忆更新成功"
}
```

---

### get_memory

**功能**: 根据 memory_id 获取指定记忆内容

**参数**:
```json
{
  "method": "get_memory",
  "params": {
    "memory_id": "string (必填) - 记忆数据 ID"
  }
}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get_memory",
    "params": {
      "memory_id": "mem_abc123"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memory": {
    "memory_id": "mem_abc123",
    "content": "用户喜欢冰美式咖啡",
    "metadata": {"category":"hobbies","type":"beverage"},
    "created_at": "2026-03-22T10:00:00Z",
    "updated_at": "2026-03-22T10:00:00Z"
  }
}
```

---

### get_all_memory

**功能**: 获取当前用户的所有记忆内容

**参数**:
```json
{
  "method": "get_all_memory",
  "params": {
    "user_id": "string (可选) - 用户身份 id",
    "run_id": "string (可选) - 会话 id",
    "agent_id": "string (可选) - 应用 id",
    "limit": "string (可选) - 返回条数，默认 100",
    "filters": "string (可选) - JSON 对象字符串，过滤条件"
  }
}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get_all_memory",
    "params": {
      "user_id": "employee_123",
      "filters": "{\"scene\":\"work\"}"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memories": [
    {
      "memory_id": "mem_work_001",
      "content": "用户负责携程 App 开发",
      "metadata": {"scene":"work","appid":"99999999"},
      "created_at": "2026-03-22T09:00:00Z"
    }
  ],
  "total": 1
}
```

---

### delete_memory

**功能**: 根据 memory_id 删除指定记忆内容

**参数**:
```json
{
  "method": "delete_memory",
  "params": {
    "memory_id": "string (必填) - 记忆数据 ID"
  }
}
```

**请求示例**:
```bash
curl -X POST http://aigw.fx.ctripcorp.com/mcp/100000013/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "delete_memory",
    "params": {
      "memory_id": "mem_abc123"
    }
  }'
```

**响应示例**:
```json
{
  "success": true,
  "memory_id": "mem_abc123",
  "message": "记忆删除成功"
}
```

---

## 💻 Python SDK 示例

### 封装类

```python
import requests
import json
from typing import Optional, Dict, List

class MCPMemoryClient:
    def __init__(self, endpoint: str = "http://aigw.fx.ctripcorp.com/mcp/100000013/mcp"):
        self.endpoint = endpoint
        self.session = requests.Session()
    
    def _call(self, method: str, params: Dict) -> Dict:
        """通用调用方法"""
        payload = {
            "method": method,
            "params": params
        }
        response = self.session.post(self.endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def add_memory(self, content: str, user_id: Optional[str] = None, 
                   metadata: Optional[Dict] = None, **kwargs) -> Dict:
        """添加记忆"""
        params = {
            "content": content,
            **({"user_id": user_id} if user_id else {}),
            **({"metadata": json.dumps(metadata)} if metadata else {}),
            **kwargs
        }
        return self._call("add_memory", params)
    
    def search_memory(self, content: str, user_id: Optional[str] = None,
                      limit: int = 100, filters: Optional[Dict] = None, **kwargs) -> Dict:
        """检索记忆"""
        params = {
            "content": content,
            **({"user_id": user_id} if user_id else {}),
            "limit": str(limit),
            **({"filters": json.dumps(filters)} if filters else {}),
            **kwargs
        }
        return self._call("search_memory", params)
    
    def update_memory(self, memory_id: str, content: str) -> Dict:
        """更新记忆"""
        return self._call("update_memory", {
            "memory_id": memory_id,
            "content": content
        })
    
    def get_memory(self, memory_id: str) -> Dict:
        """获取单条记忆"""
        return self._call("get_memory", {
            "memory_id": memory_id
        })
    
    def get_all_memory(self, user_id: Optional[str] = None,
                       limit: int = 100, filters: Optional[Dict] = None, **kwargs) -> Dict:
        """获取所有记忆"""
        params = {
            **({"user_id": user_id} if user_id else {}),
            "limit": str(limit),
            **({"filters": json.dumps(filters)} if filters else {}),
            **kwargs
        }
        return self._call("get_all_memory", params)
    
    def delete_memory(self, memory_id: str) -> Dict:
        """删除记忆"""
        return self._call("delete_memory", {
            "memory_id": memory_id
        })

# 使用示例
client = MCPMemoryClient()

# 添加记忆
result = client.add_memory(
    content="用户喜欢冰美式咖啡",
    user_id="employee_123",
    metadata={"category": "hobbies", "type": "beverage"}
)
print(f"记忆 ID: {result['memory_id']}")

# 检索记忆
results = client.search_memory(
    content="咖啡",
    user_id="employee_123",
    filters={"category": "hobbies"}
)
for memory in results['memories']:
    print(f"- {memory['content']}")

# 获取所有工作相关记忆
all_work = client.get_all_memory(
    user_id="employee_123",
    filters={"scene": "work"}
)

# 更新记忆
client.update_memory(
    memory_id="mem_abc123",
    content="用户喜欢热拿铁咖啡 (更新)"
)

# 删除记忆
client.delete_memory(memory_id="mem_abc123")
```

---

## 🎯 最佳实践

### 1. Metadata 设计规范

```python
# ✅ 推荐：清晰的分类和属性
metadata = {
    "category": "hobbies",      # 一级分类
    "type": "beverage",         # 二级分类
    "preference": "like"        # 偏好类型
}

# ✅ 推荐：项目信息
metadata = {
    "scene": "work",
    "project": "my_project",
    "language": "python",
    "framework": "flask"
}

# ❌ 避免：过于模糊
metadata = {"info": "some data"}

# ❌ 避免：嵌套过深
metadata = {"a": {"b": {"c": {"d": "value"}}}}
```

### 2. 检索优化

```python
# ✅ 推荐：使用 filters 缩小范围
client.search_memory(
    content="咖啡",
    filters={"category": "hobbies"}  # 先过滤再检索
)

# ✅ 推荐：限制返回数量
client.search_memory(
    content="咖啡",
    limit=10  # 只取最相关的 10 条
)

# ❌ 避免：无限制检索
client.search_memory(content="咖啡")  # 可能返回大量结果
```

### 3. 错误处理

```python
from requests.exceptions import RequestException

try:
    result = client.add_memory("用户偏好", user_id="employee_123")
    if result.get('success'):
        print(f"记忆 ID: {result['memory_id']}")
    else:
        print(f"添加失败：{result.get('message')}")
except RequestException as e:
    print(f"网络错误：{e}")
except Exception as e:
    print(f"未知错误：{e}")
```

### 4. 批量操作

```python
# 批量添加记忆
memories_to_add = [
    {"content": "喜欢咖啡", "metadata": {"category": "hobbies"}},
    {"content": "喜欢跑步", "metadata": {"category": "hobbies", "type": "sport"}},
    {"content": "负责携程 App", "metadata": {"scene": "work"}}
]

for mem in memories_to_add:
    client.add_memory(
        content=mem["content"],
        user_id="employee_123",
        metadata=mem["metadata"]
    )
```

---

## ⚠️ 注意事项

| 事项 | 说明 |
|------|------|
| **认证参数** | user_id/run_id/agent_id 可从 headers 自动获取 |
| **Metadata 格式** | 必须是 JSON 对象的字符串形式 |
| **Filters 对应** | 与添加记忆时的 metadata 字段对应 |
| **Limit 默认值** | 默认 100 条，建议根据场景调整 |
| **错误处理** | 检查响应中的 success 字段 |

---

## 📚 相关文档

- [企业内部记忆基建](./05-企业内部记忆基建.md) - 完整方案对比
- [AIS 平台文档](https://trip.larkenterprise.com/wiki/K1JmwT8FqipqpPk1cD2cWyAVngd) - Memobase 详细指南
- [Mem0 文档](https://docs.mem0.ai/) - 底层技术框架

---

**最后更新**: 2026-03-22  
**维护者**: AI 记忆研究组
