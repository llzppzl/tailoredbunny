"""
TailoredBunny MCP Server
为 Claude Desktop 提供 MBTI 性格适配 prompt

使用方法：
1. pip install -r requirements.txt
2. 配置 claude_desktop_config.json
3. 重启 Claude Desktop
"""

import os
import re
from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.types import Prompt, GetPromptResult

# 服务配置
SERVER_NAME = "tailoredbunny"
SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"
MEMORY_DIR = Path(__file__).parent.parent.parent / "memory"

# 初始化 Server
server = Server(SERVER_NAME)

def get_mbti_type_from_filename(filename: str) -> Optional[str]:
    """从文件名提取 MBTI 类型，如 mbti-intj.md -> intj"""
    match = re.match(r"mbti-([a-z]{4})\.md$", filename, re.IGNORECASE)
    return match.group(1).upper() if match else None

def scan_skills() -> list[dict]:
    """扫描 skills/ 目录，返回所有 MBTI prompt 列表"""
    prompts = []
    for filepath in sorted(SKILLS_DIR.glob("mbti-*.md")):
        mbti_type = get_mbti_type_from_filename(filepath.name)
        if mbti_type:
            prompts.append({
                "type": mbti_type,
                "filepath": filepath,
                "description": f"TailoredBunny {mbti_type} 性格适配"
            })
    return prompts

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """列出所有可用 prompt（用户输入 /mbti-intj 时显示）"""
    prompts = scan_skills()
    return [
        Prompt(
            name=f"mbti-{p['type'].lower()}",
            description=p["description"]
        )
        for p in prompts
    ]

@server.get_prompt()
async def get_prompt(name: str) -> GetPromptResult:
    """当用户调用 /mbti-intj 时，读取并返回对应 prompt"""
    # 提取 MBTI 类型
    mbti_type = name.replace("mbti-", "").upper()

    # 读取主 prompt
    skill_file = SKILLS_DIR / f"mbti-{mbti_type.lower()}.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"Skill file not found: {skill_file}")

    content = skill_file.read_text(encoding="utf-8")

    # 尝试加载 customized 个性化（如果存在）
    customized_file = MEMORY_DIR / f"customized-{mbti_type.lower()}.md"
    if customized_file.exists():
        customized = customized_file.read_text(encoding="utf-8")
        # 提取 ## 你的私人调整 部分
        match = re.search(r"## 你的私人调整\s*\n(.*?)$", customized, re.DOTALL | re.MULTILINE)
        if match:
            personal_adjustments = match.group(1).strip()
            content += f"\n\n## 你的私人调整\n\n{personal_adjustments}"

    return GetPromptResult(
        description=f"TailoredBunny {mbti_type} 性格适配",
        messages=[{"role": "user", "content": {"type": "text", "text": content}}]
    )

if __name__ == "__main__":
    import mcp.server.stdio
    import asyncio

    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    asyncio.run(main())
