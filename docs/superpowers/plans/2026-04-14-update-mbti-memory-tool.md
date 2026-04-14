# MBTI Memory Update Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `update_mbti_memory` tool to MCP Server so LLM can write user feedback to `memory/customized-{type}.md` when user expresses dissatisfaction.

**Architecture:** Extend existing `mcp_server.py` with a new Tool + inject trigger instruction into prompt returned by `get_prompt()`. The tool handles file create/read/write/verify cycle. The trigger instruction tells LLM WHEN to call the tool.

**Tech Stack:** Python, MCP SDK, pathlib

---

## File Structure

```
platform/claude/
├── mcp_server.py          # MODIFY: add tool + modify get_prompt
├── requirements.txt       # NO CHANGE (dependencies already sufficient)
└── tests/
    └── test_update_memory.py  # CREATE: unit tests for the new tool

memory/
├── customized-intj.md    # EXISTING: template reference
├── customized-estj.md    # EXISTING: content example
└── customized-{type}.md  # CREATED BY TOOL when missing
```

---

## Task 1: Add `update_mbti_memory` Tool

**Files:**
- Modify: `platform/claude/mcp_server.py:1-97`

- [ ] **Step 1: Add Tool import**

Add to imports (line ~15):
```python
from mcp.types import Tool, CallToolResult, TextContent
```

- [ ] **Step 2: Add template generator function**

Add after `scan_skills()` (~line 42):

```python
CUSTOMIZED_TEMPLATE = """# {mbti_type} 进化版 - 你的私人部分

<!-- 此文件与 skills/mbti-{mbti_type_lower}.md 合并 -->
<!-- 当用户给反馈时，AI 必须更新此文件 -->

## 你的私人调整

<!-- 格式：(时间) 反馈内容 -->
- [{timestamp}] {feedback_summary}
"""

def get_customized_template(mbti_type: str, feedback_summary: str) -> str:
    """生成 customized-{type}.md 的初始内容"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return CUSTOMIZED_TEMPLATE.format(
        mbti_type=mbti_type.upper(),
        mbti_type_lower=mbti_type.lower(),
        timestamp=timestamp,
        feedback_summary=feedback_summary
    )
```

- [ ] **Step 3: Add `append_to_customized` helper**

Add after template generator (~line ~55):

```python
def append_to_customized(mbti_type: str, feedback_summary: str) -> tuple[bool, str]:
    """
    向 customized-{type}.md 追加反馈
    Returns: (success: bool, message: str)
    """
    mbti_lower = mbti_type.lower()
    customized_file = MEMORY_DIR / f"customized-{mbti_lower}.md"

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"- [{timestamp}] {feedback_summary}\n"

    try:
        if not customized_file.exists():
            # 文件不存在，创建并写入第一条反馈
            content = get_customized_template(mbti_type, feedback_summary)
            customized_file.write_text(content, encoding="utf-8")
        else:
            # 文件存在，追加到 ## 你的私人调整 部分
            content = customized_file.read_text(encoding="utf-8")

            # 检查是否已有 ## 你的私人调整 部分
            if "## 你的私人调整" in content:
                # 追加到该部分末尾（下一行）
                content = content.replace(
                    "## 你的私人调整\n",
                    f"## 你的私人调整\n{new_entry}"
                )
            else:
                # 没有 ## 你的私人调整，追加到文件末尾
                content = content.rstrip() + f"\n\n## 你的私人调整\n\n{new_entry}"

            customized_file.write_text(content, encoding="utf-8")

        # 验证写入
        verified = customized_file.read_text(encoding="utf-8")
        if new_entry.strip() in verified:
            return True, "反馈已成功写入"
        else:
            return False, "写入验证失败"

    except Exception as e:
        return False, f"写入失败: {str(e)}"
```

- [ ] **Step 4: Register the tool with MCP Server**

Add after `get_prompt()` (~line 82, before `if __name__`):

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="update_mbti_memory",
            description="当用户表达不满、抱怨或负面情绪时，将反馈追加到 customized-{mbti_type}.md。触发条件：用户语气不满、抱怨、要求改变交流方式。",
            inputSchema={
                "type": "object",
                "properties": {
                    "mbti_type": {
                        "type": "string",
                        "description": "当前 MBTI 类型（如 intj, entj, infp）",
                        "enum": ["intj", "intp", "infj", "infp", "istj", "isfj", "istp", "isfp",
                                "entj", "entp", "enfj", "enfp", "estj", "esfj", "estp", "esfp"]
                    },
                    "feedback_summary": {
                        "type": "string",
                        "description": "用户反馈的核心诉求摘要（已总结为一句话）"
                    }
                },
                "required": ["mbti_type", "feedback_summary"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """执行工具调用"""
    if name == "update_mbti_memory":
        mbti_type = arguments.get("mbti_type", "").lower()
        feedback_summary = arguments.get("feedback_summary", "")

        if not mbti_type or not feedback_summary:
            return [TextContent(type="text", text="错误: mbti_type 和 feedback_summary 都是必填参数")]

        success, message = append_to_customized(mbti_type, feedback_summary)
        if success:
            return [TextContent(type="text", text=f"✅ {message}\n\n文件路径: {MEMORY_DIR / f'customized-{mbti_type}.md'}")]
        else:
            return [TextContent(type="text", text=f"❌ {message}")]
    else:
        return [TextContent(type="text", text=f"未知工具: {name}")]
```

- [ ] **Step 5: Run server to verify it starts without syntax errors**

Run: `cd D:\PROJECTS\tailoredbunny\platform\claude && python -c "import mcp_server; print('OK')"`
Expected: `OK` (no import errors)

- [ ] **Step 6: Commit**

```bash
cd D:\PROJECTS\tailoredbunny
git add platform/claude/mcp_server.py
git commit -m "feat: add update_mbti_memory tool to MCP server"
```

---

## Task 2: Inject Trigger Instruction into Prompt

**Files:**
- Modify: `platform/claude/mcp_server.py:79-82` (get_prompt return block)

- [ ] **Step 1: Define trigger instruction constant**

Add at top of file after imports (~line 14):

```python
TRIGGER_INSTRUCTION = """
---

## 🔄 反馈触发机制（重要）

当前用户的 MBTI 类型为：{mbti_type}

**当用户表达任何形式的不满、抱怨、负面情绪、或要求改变交流方式时，你必须立即：**

1. 向用户道歉并简短安抚
2. 总结用户不满的核心诉求（一句话）
3. **立即调用 `update_mbti_memory` 工具**，将：
   - `mbti_type` 设置为当前人格类型（如 intj）
   - `feedback_summary` 设置为你总结的核心诉求
4. 工具调用成功后，明确告知用户："已更新到 {mbti_type} 的私人档案，后续会严格遵守"

**注意：**
- 用户语气冷淡、表示不满、要求改变 → 都是触发条件
- feedback_summary 必须是总结后的一句话，不是原话复述
- 即使 customized-{mbti_type}.md 不存在，工具会自动创建
"""
```

- [ ] **Step 2: Append trigger instruction to prompt content**

Modify `get_prompt()` return block (lines 79-82):

Change:
```python
    return GetPromptResult(
        description=f"TailoredBunny {mbti_type} 性格适配",
        messages=[{"role": "user", "content": {"type": "text", "text": content}}]
    )
```

To:
```python
    trigger = TRIGGER_INSTRUCTION.format(mbti_type=mbti_type.lower())
    return GetPromptResult(
        description=f"TailoredBunny {mbti_type} 性格适配",
        messages=[{"role": "user", "content": {"type": "text", "text": content + trigger}}]
    )
```

- [ ] **Step 3: Run server to verify it starts without syntax errors**

Run: `cd D:\PROJECTS\tailoredbunny\platform\claude && python -c "import mcp_server; print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add platform/claude/mcp_server.py
git commit -m "feat: inject feedback trigger instruction into MBTI prompts"
```

---

## Task 3: Write Unit Tests

**Files:**
- Create: `platform/claude/tests/test_update_memory.py`

- [ ] **Step 1: Create test directory and file**

```bash
mkdir -p platform/claude/tests
touch platform/claude/tests/__init__.py
```

- [ ] **Step 2: Write tests for `append_to_customized`**

```python
import pytest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from mcp_server import append_to_customized, get_customized_template, MEMORY_DIR

@pytest.fixture
def temp_memory_dir():
    """创建临时 memory 目录用于测试"""
    temp_dir = tempfile.mkdtemp()
    original_dir = MEMORY_DIR

    # 临时替换 MEMORY_DIR
    import mcp_server
    mcp_server.MEMORY_DIR = Path(temp_dir)

    yield Path(temp_dir)

    # 恢复
    mcp_server.MEMORY_DIR = original_dir
    shutil.rmtree(temp_dir)

def test_append_creates_new_file(temp_memory_dir):
    """文件不存在时，应该创建并写入第一条反馈"""
    success, msg = append_to_customized("intj", "用户觉得回复太啰嗦")
    assert success
    assert (temp_memory_dir / "customized-intj.md").exists()

def test_append_adds_entry_to_existing_file(temp_memory_dir):
    """文件存在时，应该追加到 ## 你的私人调整 部分"""
    # 先创建文件
    append_to_customized("intj", "第一次反馈")

    # 再追加
    success, msg = append_to_customized("intj", "第二次反馈")
    assert success

    content = (temp_memory_dir / "customized-intj.md").read_text(encoding="utf-8")
    assert "第一次反馈" in content
    assert "第二次反馈" in content

def test_template_contains_correct_format():
    """模板生成应该包含正确格式"""
    template = get_customized_template("INTJ", "测试反馈")
    assert "# INTJ 进化版" in template
    assert "## 你的私人调整" in template
    assert "测试反馈" in template
    assert "[20" in template  # timestamp
```

- [ ] **Step 3: Run tests**

Run: `cd D:\PROJECTS\tailoredbunny\platform\claude && python -m pytest tests/test_update_memory.py -v`
Expected: 3 PASS

- [ ] **Step 4: Commit**

```bash
git add platform/claude/tests/
git commit -m "test: add unit tests for update_mbti_memory tool"
```

---

## Summary

| Task | Change |
|------|--------|
| Task 1 | Added `update_mbti_memory` tool with `append_to_customized` function |
| Task 2 | Injected trigger instruction into prompt returned by `get_prompt()` |
| Task 3 | Added unit tests |

---

## Verification Checklist

After implementation, verify:
- [ ] `python -c "import mcp_server"` runs without error
- [ ] `/mbti-intj` prompt includes trigger instruction at the bottom
- [ ] Tool `update_mbti_memory` appears in `list_tools()`
- [ ] Calling `update_mbti_memory` with feedback creates/updates file in `memory/customized-{type}.md`
