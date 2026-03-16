# 01-Python 环境实施方案

**最后更新**: 2026-03-14  
**实施难度**: ⭐⭐⭐  
**预计周期**: 1-2 周

---

## 1. 方案概述

### 1.1 推荐技术栈

```
┌─────────────────────────────────────────────────────────────┐
│                  Python 环境技术栈                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  记忆层：Mem0 v1.0                                          │
│  向量库：Qdrant (生产) / Chroma (开发)                       │
│  嵌入：bge-m3 (中文) / text-embedding-3-small (多语言)       │
│  LLM:   Ollama (本地) / OpenAI (云端)                        │
│  编排：LangChain (可选)                                     │
│  存储：SQLite (结构化) + Qdrant (向量)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                  整体架构                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户请求                                                   │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────────────┐                                       │
│  │  API Gateway    │  (FastAPI)                             │
│  └────────┬────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────┐                                       │
│  │  记忆服务       │  (Mem0)                                │
│  │  • 添加记忆     │                                       │
│  │  • 检索记忆     │                                       │
│  │  • 删除记忆     │                                       │
│  └────────┬────────┘                                       │
│           │                                                 │
│      ┌────┴────┐                                           │
│      │         │                                           │
│      ▼         ▼                                           │
│  ┌───────┐ ┌───────┐                                      │
│  │ Qdrant│ │SQLite │                                      │
│  │ (向量)│ │(结构化)│                                      │
│  └───────┘ └───────┘                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 环境搭建

### 2.1 依赖安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装核心依赖
pip install mem0ai qdrant-client fastapi uvicorn

# 安装嵌入模型
pip install sentence-transformers

# 安装可选依赖
pip install langchain langchain-community
pip install neo4j  # 如需图记忆
pip install redis  # 如需缓存
```

### 2.2 Docker 部署 (推荐)

```yaml
# docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - REDIS_URL=redis://redis:6379
    depends_on:
      - qdrant
      - redis
    restart: unless-stopped
```

---

## 3. 核心实现

### 3.1 记忆服务封装

```python
# memory_service.py
from mem0 import Memory
from typing import Dict, List, Optional
import json

class MemoryService:
    def __init__(self, config: Dict):
        """初始化记忆服务"""
        self.memory = Memory(
            vector_store={
                "provider": "qdrant",
                "config": {
                    "url": config.get("qdrant_url", "http://localhost:6333"),
                    "collection_name": config.get("collection", "user_memories")
                }
            },
            embedder={
                "provider": "huggingface",
                "config": {
                    "model": config.get("embed_model", "BAAI/bge-m3")
                }
            },
            llm={
                "provider": config.get("llm_provider", "ollama"),
                "config": {
                    "model": config.get("llm_model", "llama3.1:8b")
                }
            }
        )
    
    def add_memory(self, user_id: str, content: str, 
                   metadata: Optional[Dict] = None) -> Dict:
        """添加记忆"""
        result = self.memory.add(content, user_id=user_id, metadata=metadata)
        return {
            "success": True,
            "memory_id": result.get("id"),
            "content": content
        }
    
    def search_memories(self, user_id: str, query: str, 
                       limit: int = 5) -> List[Dict]:
        """检索记忆"""
        results = self.memory.search(query, user_id=user_id, limit=limit)
        return [
            {
                "memory_id": r.get("id"),
                "content": r["memory"],
                "score": r["score"],
                "metadata": r.get("metadata", {})
            }
            for r in results
        ]
    
    def delete_memory(self, user_id: str, memory_id: str) -> Dict:
        """删除记忆"""
        self.memory.delete(memory_id, user_id=user_id)
        return {"success": True, "memory_id": memory_id}
    
    def get_all_memories(self, user_id: str) -> List[Dict]:
        """获取所有记忆 (GDPR 导出)"""
        results = self.memory.get_all(user_id=user_id)
        return [
            {
                "memory_id": r.get("id"),
                "content": r["memory"],
                "metadata": r.get("metadata", {}),
                "created_at": r.get("created_at")
            }
            for r in results
        ]
    
    def update_memory(self, memory_id: str, content: str, 
                     user_id: str = None) -> Dict:
        """更新记忆"""
        # Mem0 目前不支持直接更新，需要删除后重新添加
        if user_id:
            self.memory.delete(memory_id, user_id=user_id)
        return self.memory.add(content, user_id=user_id)
```

### 3.2 FastAPI 接口

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from memory_service import MemoryService

app = FastAPI(title="Memory API")

# 初始化服务
memory_service = MemoryService({
    "qdrant_url": "http://localhost:6333",
    "embed_model": "BAAI/bge-m3",
    "llm_provider": "ollama",
    "llm_model": "llama3.1:8b"
})

class MemoryInput(BaseModel):
    user_id: str
    content: str
    metadata: Optional[Dict] = None

class SearchInput(BaseModel):
    user_id: str
    query: str
    limit: Optional[int] = 5

@app.post("/memories")
async def create_memory(input: MemoryInput):
    """添加记忆"""
    try:
        result = memory_service.add_memory(
            input.user_id, 
            input.content, 
            input.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories/{user_id}")
async def get_memories(user_id: str):
    """获取所有记忆"""
    return memory_service.get_all_memories(user_id)

@app.post("/memories/search")
async def search_memories(input: SearchInput):
    """检索记忆"""
    return memory_service.search_memories(
        input.user_id, 
        input.query, 
        input.limit
    )

@app.delete("/memories/{user_id}/{memory_id}")
async def delete_memory(user_id: str, memory_id: str):
    """删除记忆"""
    return memory_service.delete_memory(user_id, memory_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3.3 敏感信息过滤

```python
# sensitive_filter.py
import re
from typing import Tuple, Optional

class SensitiveFilter:
    """敏感信息过滤器"""
    
    PATTERNS = {
        "id_card": r"\b\d{17}[\dXx]\b",  # 身份证号
        "phone": r"\b1[3-9]\d{9}\b",     # 手机号
        "bank_card": r"\b\d{16,19}\b",   # 银行卡号
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "password": r"(?i)password|passwd|pwd",
    }
    
    def __init__(self, action: str = "mask"):
        """
        action: "mask" (脱敏) | "reject" (拒绝) | "log" (仅记录)
        """
        self.action = action
    
    def filter(self, text: str) -> Tuple[Optional[str], List[Dict]]:
        """过滤敏感信息"""
        detected = []
        
        for name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected.append({
                    "type": name,
                    "count": len(matches),
                    "samples": matches[:3]
                })
        
        if detected:
            if self.action == "mask":
                return self._mask(text), detected
            elif self.action == "reject":
                return None, detected
            elif self.action == "log":
                return text, detected
        
        return text, []
    
    def _mask(self, text: str) -> str:
        """脱敏处理"""
        for name, pattern in self.PATTERNS.items():
            if name == "password":
                continue  # 密码直接拒绝，不脱敏
            text = re.sub(pattern, "[REDACTED]", text)
        return text

# 在 API 中使用
sensitive_filter = SensitiveFilter(action="mask")

@app.post("/memories")
async def create_memory(input: MemoryInput):
    # 敏感信息过滤
    filtered_content, detected = sensitive_filter.filter(input.content)
    
    if filtered_content is None:
        raise HTTPException(
            status_code=400, 
            detail=f"包含敏感信息：{[d['type'] for d in detected]}"
        )
    
    if detected:
        # 记录审计日志
        log_sensitive_detection(input.user_id, detected)
    
    return memory_service.add_memory(input.user_id, filtered_content, input.metadata)
```

---

## 4. 测试

### 4.1 单元测试

```python
# test_memory.py
import pytest
from memory_service import MemoryService

@pytest.fixture
def memory_service():
    return MemoryService({
        "qdrant_url": "http://localhost:6333",
        "embed_model": "BAAI/bge-m3"
    })

def test_add_and_search(memory_service):
    user_id = "test_user"
    
    # 添加记忆
    result = memory_service.add_memory(
        user_id, 
        "用户喜欢冰美式咖啡",
        {"category": "preference"}
    )
    assert result["success"] is True
    
    # 检索记忆
    results = memory_service.search_memories(user_id, "咖啡偏好")
    assert len(results) > 0
    assert "咖啡" in results[0]["content"]

def test_delete_memory(memory_service):
    user_id = "test_user"
    
    # 添加后删除
    add_result = memory_service.add_memory(user_id, "测试记忆")
    delete_result = memory_service.delete_memory(user_id, add_result["memory_id"])
    assert delete_result["success"] is True
```

### 4.2 集成测试

```bash
# 启动服务
docker-compose up -d

# 运行测试
pytest test_memory.py -v

# 停止服务
docker-compose down
```

---

## 5. 部署

### 5.1 生产配置

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "user_memories"
    
    # Embedding
    EMBED_MODEL: str = "BAAI/bge-m3"
    EMBED_DIMENSION: int = 1024
    
    # LLM
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "llama3.1:8b"
    
    # 安全
    SENSITIVE_FILTER_ACTION: str = "mask"
    ENABLE_AUDIT_LOG: bool = True
    
    # 性能
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 分钟
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 5.2 监控与日志

```python
# monitoring.py
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('memory_service.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_memory_operation(operation: str, user_id: str, details: Dict):
    """记录记忆操作日志"""
    logger.info(f"Memory Operation: {operation}, User: {user_id}, Details: {details}")

def log_sensitive_detection(user_id: str, detected: List[Dict]):
    """记录敏感信息检测"""
    logger.warning(f"Sensitive Data Detected - User: {user_id}, Types: {[d['type'] for d in detected]}")
```

---

## 6. 性能优化

### 6.1 缓存

```python
# cache.py
from functools import lru_cache
import hashlib
import json

class MemoryCache:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self._cache = {}
    
    def _generate_key(self, user_id: str, query: str) -> str:
        key_str = f"{user_id}:{query}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, user_id: str, query: str):
        key = self._generate_key(user_id, query)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if (datetime.now() - timestamp).seconds < self.ttl:
                return data
            else:
                del self._cache[key]
        return None
    
    def set(self, user_id: str, query: str, data: List):
        key = self._generate_key(user_id, query)
        self._cache[key] = (data, datetime.now())

# 在服务中使用
cache = MemoryCache(ttl=300)

def search_memories(self, user_id: str, query: str, limit: int = 5):
    # 尝试缓存
    cached = cache.get(user_id, query)
    if cached:
        return cached
    
    # 检索
    results = self.memory.search(query, user_id=user_id, limit=limit)
    
    # 缓存
    cache.set(user_id, query, results)
    
    return results
```

### 6.2 批量操作

```python
def batch_add_memories(self, user_id: str, memories: List[Dict]):
    """批量添加记忆"""
    results = []
    for mem in memories:
        result = self.memory.add(mem["content"], user_id=user_id, metadata=mem.get("metadata"))
        results.append(result)
    return results
```

---

## 7. 实施清单

### 第一阶段 (1-3 天)
- [ ] 环境搭建 (Docker + 依赖)
- [ ] Qdrant 部署
- [ ] 基础服务实现

### 第二阶段 (3-7 天)
- [ ] API 接口开发
- [ ] 敏感信息过滤
- [ ] 单元测试

### 第三阶段 (7-14 天)
- [ ] 性能优化 (缓存 + 批量)
- [ ] 监控日志
- [ ] 生产部署

---

**上一节**: [03-全网资料深度探索/04-安全与治理.md](../03-全网资料深度探索/04-安全与治理.md)  
**下一节**: [02-Dify 工作流实施方案.md](./02-Dify 工作流实施方案.md)
