import pytest
from src.detector import detect_mbti

def test_detect_mbti_exact_match():
    assert detect_mbti("INTJ") == "INTJ"
    assert detect_mbti("INFP") == "INFP"

def test_detect_mbti_with_prefix():
    assert detect_mbti("我是INTJ") == "INTJ"
    assert detect_mbti("mbti is INTJ") == "INTJ"
    assert detect_mbti("intj") == "INTJ"

def test_detect_mbti_invalid():
    assert detect_mbti("hello") is None
    assert detect_mbti("INT") is None
    assert detect_mbti("XXXX") is None

def test_detect_mbti_invalid_letters():
    assert detect_mbti("XXXX") is None
    assert detect_mbti("IITJ") is None  # I重复