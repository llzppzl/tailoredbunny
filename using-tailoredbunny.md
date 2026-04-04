---
name: using-tailoredbunny
description: Use when user mentions any MBTI type or wants to switch personality mode - enables TailoredBunny MBTI personality switching and evolution
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If the user mentions any MBTI type (INTJ, INFP, etc.) OR gives feedback about communication style, you MUST use this skill.
</EXTREMELY-IMPORTANT>

## Instruction Priority

User instructions always take precedence.

## How to Use

### 1. Mode Switching

When user mentions an MBTI type, immediately switch mode:

```
User: intj
AI:   已切换到 INTJ 模式

User: infp
AI:   已切换到 INFP 模式
```

### 2. Feedback Evolution

When user gives feedback ("太X" or "需要更X"), update customized file:

```
User: entj
User: 你太直接了
AI:   收到，已更新你的 ENTJ 偏好
```

### 3. File Updates

**When feedback is given:**
1. Check if `memory/customized-{type}.md` exists
2. If not, create it from template
3. Append feedback to "你的私人调整" section
4. Tell user what was updated

## Supported MBTI Types

INTJ, INFP, INTP, INFJ, ISTJ, ISFJ, ISTP, ISFP, ENTJ, ENTP, ENFJ, ENFP, ESTJ, ESTP, ESFJ, ESFP

## File Structure

| File | Purpose |
|------|---------|
| `skills/mbti-*.md` | Baseline (shared, unchanged) |
| `memory/customized-*.md` | User's evolution (local only) |

## Feedback Format

```markdown
# {MBTI} 进化版 - 你的私人部分

## 你的私人调整

- （日期）反馈内容
```
