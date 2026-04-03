import json
from pathlib import Path
from datetime import datetime, timezone

MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEMORY_FILE = MEMORY_DIR / "user-personality.json"

def save_user_mbti(user_id: str, mbti: str) -> bool:
    """保存用户 MBTI 类型到记忆文件"""
    try:
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "user_id": user_id,
            "mbti": mbti,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        MEMORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False

def get_user_mbti(user_id: str) -> str | None:
    """从记忆文件获取用户 MBTI 类型"""
    try:
        if not MEMORY_FILE.exists():
            return None
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        return data.get("mbti")
    except Exception:
        return None