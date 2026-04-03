import json
import pytest
from pathlib import Path
from src.memory import save_user_mbti, get_user_mbti, MEMORY_FILE

def test_save_and_get_user_mbti():
    # 先清除可能存在的记忆
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()

    result = save_user_mbti("default", "INTJ")
    assert result is True
    assert MEMORY_FILE.exists()

    mbti = get_user_mbti("default")
    assert mbti == "INTJ"

def test_get_nonexistent_user():
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()
    assert get_user_mbti("nonexistent") is None