from src.detector import detect_mbti
from src.loader import load_preset
from src.memory import save_user_mbti as memory_save, get_user_mbti as memory_get

def get_preset(mbti: str) -> str:
    """获取 MBTI 预设内容"""
    return load_preset(mbti) or ""

def save_user_mbti(user_id: str, mbti: str) -> bool:
    """保存用户 MBTI 类型"""
    return memory_save(user_id, mbti)

def get_user_mbti(user_id: str) -> str | None:
    """获取用户 MBTI 类型"""
    return memory_get(user_id)

def detect_mbti_from_text(text: str) -> str | None:
    """从文本中检测 MBTI 类型"""
    return detect_mbti(text)
