import pytest
from mcp.server import get_preset, save_user_mbti, get_user_mbti, detect_mbti_from_text

def test_get_preset():
    result = get_preset("INTJ")
    assert result is not None
    assert "冷酷幕僚长" in result

def test_save_and_get_user_mbti():
    from src.memory import MEMORY_FILE
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()

    assert save_user_mbti("test", "INFP") is True
    assert get_user_mbti("test") == "INFP"

def test_detect_mbti_from_text():
    assert detect_mbti_from_text("我是INTJ") == "INTJ"
