"""
长期记忆服务示例 - Python 实现

功能:
- 添加记忆
- 检索记忆
- 删除记忆
- 批量操作

依赖:
    pip install mem0ai qdrant-client

使用:
    python memory_service.py
"""

from mem0 import Memory
from typing import Dict, List, Optional
import json


class MemoryService:
    """记忆服务类"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化记忆服务
        
        Args:
            config: 配置字典，示例:
                {
                    "qdrant_url": "http://localhost:6333",
                    "embed_model": "BAAI/bge-m3",
                    "llm_provider": "ollama",
                    "llm_model": "llama3.1:8b"
                }
        """
        if config is None:
            config = {
                "qdrant_url": "http://localhost:6333",
                "embed_model": "BAAI/bge-m3",
                "llm_provider": "ollama",
                "llm_model": "llama3.1:8b"
            }
        
        self.memory = Memory(
            vector_store={
                "provider": "qdrant",
                "config": {
                    "url": config.get("qdrant_url", "http://localhost:6333"),
                    "collection_name": "user_memories"
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
        """
        添加记忆
        
        Args:
            user_id: 用户 ID
            content: 记忆内容
            metadata: 元数据，如 {"category": "preference", "sensitivity": "low"}
        
        Returns:
            包含 memory_id 的字典
        """
        result = self.memory.add(content, user_id=user_id, metadata=metadata)
        return {
            "success": True,
            "memory_id": result.get("id"),
            "content": content
        }
    
    def search_memories(self, user_id: str, query: str, 
                       limit: int = 5) -> List[Dict]:
        """
        检索记忆
        
        Args:
            user_id: 用户 ID
            query: 查询文本
            limit: 返回数量限制
        
        Returns:
            记忆列表
        """
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
        """
        删除记忆
        
        Args:
            user_id: 用户 ID
            memory_id: 记忆 ID
        
        Returns:
            删除结果
        """
        self.memory.delete(memory_id, user_id=user_id)
        return {"success": True, "memory_id": memory_id}
    
    def get_all_memories(self, user_id: str) -> List[Dict]:
        """
        获取所有记忆 (GDPR 导出)
        
        Args:
            user_id: 用户 ID
        
        Returns:
            所有记忆列表
        """
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
    
    def batch_add_memories(self, user_id: str, memories: List[Dict]) -> List[Dict]:
        """
        批量添加记忆
        
        Args:
            user_id: 用户 ID
            memories: 记忆列表，每项包含 content 和 metadata
        
        Returns:
            添加结果列表
        """
        results = []
        for mem in memories:
            result = self.add_memory(user_id, mem["content"], mem.get("metadata"))
            results.append(result)
        return results


def demo():
    """演示使用"""
    print("🧠 长期记忆服务演示\n")
    
    # 初始化服务
    service = MemoryService()
    
    # 添加记忆
    print("📝 添加记忆...")
    service.add_memory("user_123", "用户喜欢冰美式咖啡", 
                      {"category": "preference"})
    service.add_memory("user_123", "用户居住在北京", 
                      {"category": "fact"})
    service.add_memory("user_123", "用户是软件工程师", 
                      {"category": "profile"})
    print("✅ 记忆添加完成\n")
    
    # 检索记忆
    print("🔍 检索记忆 (咖啡偏好)...")
    results = service.search_memories("user_123", "咖啡偏好")
    for r in results:
        print(f"  - {r['content']} (得分：{r['score']:.2f})")
    print()
    
    # 获取所有记忆
    print("📋 所有记忆:")
    all_memories = service.get_all_memories("user_123")
    for mem in all_memories:
        print(f"  - {mem['content']} [{mem.get('metadata', {}).get('category', 'N/A')}]")
    print()
    
    # 删除记忆
    if all_memories:
        print("🗑️  删除记忆...")
        service.delete_memory("user_123", all_memories[0]["memory_id"])
        print("✅ 记忆删除完成\n")


if __name__ == "__main__":
    demo()
