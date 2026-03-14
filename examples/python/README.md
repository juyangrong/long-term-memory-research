# Python 示例代码

本目录包含长期记忆系统的 Python 代码示例。

## 文件说明

| 文件 | 功能 | 依赖 |
|------|------|------|
| `memory_service.py` | 记忆服务封装 | mem0ai, qdrant-client |
| `sensitive_filter.py` | 敏感信息过滤 | 无 |
| `personal_assistant.py` | 个人助理示例 | sqlite3 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行示例

```bash
# 记忆服务演示
python memory_service.py

# 敏感信息过滤演示
python sensitive_filter.py

# 个人助理演示
python personal_assistant.py
```

## 集成到你的项目

### 记忆服务

```python
from memory_service import MemoryService

service = MemoryService({
    "qdrant_url": "http://localhost:6333"
})

# 添加记忆
service.add_memory("user_123", "用户喜欢咖啡")

# 检索记忆
results = service.search_memories("user_123", "咖啡偏好")
```

### 敏感信息过滤

```python
from sensitive_filter import SensitiveFilter

filter = SensitiveFilter(action="mask")
text = "我的手机号是 13800138000"
filtered, detected = filter.filter(text)
```

## 详细文档

完整实施指南见：[docs/04-落地实施方案/01-Python 环境实施方案.md](../docs/04-落地实施方案/01-Python 环境实施方案.md)
