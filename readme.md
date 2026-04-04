# TailoredBunny

让 AI Agent 拥有"性格"的项目。像切换 skill 一样，随时切换 MBTI 人格模式。

## 核心功能

**MBTI 模式切换** - 说 `infp` 或 `intj`，AI 立即切换对话风格

```
用户: infp
AI:   已切换到 INFP 模式

用户: intj
AI:   已切换到 INTJ 模式
```

## 使用方式

在 Claude Code 中加载项目后，说出 MBTI 类型即可切换：
- `infp` → 知心搭档模式（温和、支持、每次一点点）
- `intj` → 冷酷幕僚长模式（直接给结论、MECE 表格）

预设内容在 `skills/mbti-*.md`，可自行添加更多类型。

## 支持的 MBTI 类型

- INTJ - 冷酷幕僚长
- INFP - 知心搭档

## 开发

```bash
# 运行测试
python -m pytest tests/ -v
```
