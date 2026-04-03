import re

MBTI_PATTERN = re.compile(r'(?<![a-zA-Z])([IE][NS][TF][JP])(?![a-zA-Z])', re.IGNORECASE)

def detect_mbti(user_input: str) -> str | None:
    """
    解析用户输入，识别 MBTI 类型
    返回: "INTJ" | "INFP" | None（无法识别）
    """
    if not user_input:
        return None

    match = MBTI_PATTERN.search(user_input.upper())
    if match:
        return match.group(1)
    return None