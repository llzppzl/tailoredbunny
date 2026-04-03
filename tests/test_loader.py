import pytest
from src.loader import load_preset, PRESETS_DIR

def test_load_preset_intj():
    result = load_preset("INTJ")
    assert result is not None
    assert "INTJ" in result
    assert "冷酷幕僚长" in result

def test_load_preset_infp():
    result = load_preset("INFP")
    assert result is not None
    assert "INFP" in result
    assert "知心搭档" in result

def test_load_preset_not_found():
    result = load_preset("ENTJ")
    assert result is None