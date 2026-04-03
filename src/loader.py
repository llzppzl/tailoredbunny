from pathlib import Path

PRESETS_DIR = Path(__file__).parent.parent / "presets"

def load_preset(mbti: str) -> str | None:
    """
    加载对应 MBTI 的预设
    返回: 预设文件内容 | None（预设不存在）
    """
    if not mbti:
        return None

    # 查找 preset-{mbti.lower()}-*.md
    pattern = f"preset-{mbti.lower()}-"
    for preset_file in PRESETS_DIR.glob(f"{pattern}*.md"):
        return preset_file.read_text(encoding="utf-8")

    return None