"""
敏感信息过滤器

功能:
- 检测敏感信息 (身份证号、手机号、银行卡等)
- 脱敏处理
- 拒绝或记录

使用:
    from sensitive_filter import SensitiveFilter
    
    filter = SensitiveFilter(action="mask")
    text = "我的手机号是 13800138000"
    filtered, detected = filter.filter(text)
"""

import re
from typing import List, Dict, Tuple, Optional


class SensitiveFilter:
    """敏感信息过滤器"""
    
    # 敏感信息模式
    PATTERNS = {
        "id_card": r"\b\d{17}[\dXx]\b",  # 身份证号
        "phone": r"\b1[3-9]\d{9}\b",     # 手机号
        "bank_card": r"\b\d{16,19}\b",   # 银行卡号
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "password": r"(?i)password|passwd|pwd",
        "address": r"(?i)地址 | 住址 | 街道 | 小区 | 号楼",
    }
    
    # 敏感度分级
    SENSITIVITY_LEVELS = {
        "high": ["id_card", "bank_card", "password", "health"],
        "medium": ["phone", "email", "address"],
        "low": ["preference", "habit"]
    }
    
    def __init__(self, action: str = "mask"):
        """
        初始化过滤器
        
        Args:
            action: 处理方式
                - "mask": 脱敏
                - "reject": 拒绝
                - "log": 仅记录
        """
        self.action = action
    
    def filter(self, text: str) -> Tuple[Optional[str], List[Dict]]:
        """
        过滤敏感信息
        
        Args:
            text: 输入文本
        
        Returns:
            (处理后的文本，检测到的敏感信息列表)
            如果 action="reject" 且检测到高敏感信息，返回 (None, detected)
        """
        detected = []
        
        # 检测敏感信息
        for name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected.append({
                    "type": name,
                    "count": len(matches),
                    "level": self._get_level(name),
                    "samples": matches[:3]  # 只保留前 3 个样本
                })
        
        # 检查是否有高敏感信息
        high_sensitivity = any(d["level"] == "high" for d in detected)
        
        if high_sensitivity and self.action == "reject":
            return None, detected
        
        # 处理
        if detected:
            if self.action == "mask":
                return self._mask(text), detected
            elif self.action == "log":
                return text, detected
        
        return text, []
    
    def _get_level(self, pattern_name: str) -> str:
        """获取敏感度级别"""
        for level, patterns in self.SENSITIVITY_LEVELS.items():
            if pattern_name in patterns:
                return level
        return "low"
    
    def _mask(self, text: str) -> str:
        """脱敏处理"""
        for name, pattern in self.PATTERNS.items():
            if name == "password":
                continue  # 密码直接拒绝，不脱敏
            text = re.sub(pattern, "[REDACTED]", text)
        return text
    
    def filter_batch(self, texts: List[str]) -> List[Tuple[Optional[str], List[Dict]]]:
        """批量过滤"""
        return [self.filter(text) for text in texts]


def demo():
    """演示使用"""
    print("🔒 敏感信息过滤器演示\n")
    
    # 创建过滤器
    filter = SensitiveFilter(action="mask")
    
    # 测试用例
    test_cases = [
        "我的手机号是 13800138000",
        "身份证号：110101199001011234",
        "邮箱：test@example.com",
        "我喜欢喝咖啡",  # 无敏感信息
        "密码是 password123",  # 高敏感
    ]
    
    for text in test_cases:
        print(f"原文：{text}")
        filtered, detected = filter.filter(text)
        
        if filtered is None:
            print(f"结果：❌ 拒绝 (包含高敏感信息)")
        elif detected:
            print(f"结果：{filtered}")
        else:
            print(f"结果：✅ 无敏感信息")
        
        if detected:
            print(f"检测到：{detected}")
        print()


if __name__ == "__main__":
    demo()
