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

## 文件结构

| 文件 | 用途 |
|------|------|
| `skills/mbti-*.md` | 通用 baseline（不变） |
| `memory/customized-*.md` | 你的私人进化版 |

## 进化机制

**Baseline** = 通用 INTJ/INFP 风格（不变）
**Customized** = 你的私人调整（会累积）

切换模式时，两者**合并** = 完整的风格

**怎么进化：**
1. 你给反馈（如"太啰嗦了"）
2. AI 更新 `memory/customized-*.md`
3. 下次加载时，你的私人部分增强

## 使用方式

在 Claude Code 中加载项目后：
- `infp` → 知心搭档模式（温和、支持、每次一点点）
- `intj` → 冷酷幕僚长模式（直接给结论、MECE 表格）

## 支持的 MBTI 类型

- INTJ - 冷酷幕僚长
- INFP - 知心搭档

## 开发

```bash
# 运行测试
python -m pytest tests/ -v
```
