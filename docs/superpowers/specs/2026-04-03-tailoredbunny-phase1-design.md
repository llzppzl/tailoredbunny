# TailoredBunny Phase 1 设计文档

> **状态**: 已更新
> **日期**: 2026-04-04
> **更新说明**: 改为 skill-based MBTI 模式切换，而非 AI 自动检测

## 概述

TailoredBunny 是一个让 AI Agent 拥有"性格"的项目。像切换 superpowers skill 一样，随时切换 MBTI 人格模式。

**Phase 1 目标**: 实现 MBTI 模式切换 —— 用户说 `infp` 或 `intj`，AI 立即切换对话风格。

---

## 核心流程

```
用户: infp
    ↓
AI 加载 skills/mbti-infp.md
    ↓
切换到 INFP 知心搭档模式
    ↓
用户: intj
    ↓
AI 加载 skills/mbti-intj.md
    ↓
切换到 INTJ 冷酷幕僚长模式
```

---

## 文件结构

```
tailoredbunny/
├── skills/
│   ├── mbti-intj.md           # INTJ 预设
│   └── mbti-infp.md          # INFP 预设
├── presets/
│   ├── intro-prompt.md        # 入口引导（备用）
│   ├── preset-intj-strategist.md
│   └── preset-infp-companion.md
├── src/
│   ├── detector.py            # MBTI 检测器
│   ├── loader.py               # 预设加载器
│   └── memory.py               # 记忆模块
├── memory/
│   └── user-personality.json
├── tests/
├── docs/
├── CLAUDE.md                   # 项目说明（自动加载）
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 实现方式

### MBTI Skill 文件 (`skills/mbti-{type}.md`)

**职责**: 定义每种 MBTI 类型的交互风格

**INTJ 预设结构**:
```markdown
# INTJ - 冷酷幕僚长

## 风格
- 直接给结论
- 不废话
- MECE 表格
- 风险评估

## 交互层
- N型（要底层逻辑、战略视角）
- T型（冷酷逻辑、直击痛点）
- I型（直接给结论、减少确认）
- 输出格式: MECE 表格 + 风险评估

## 架构层
- J型（瀑布流、WBS、节点验收）
- 红蓝对抗: 开启

## 记忆层
- 雷区: [避免废话、避免不确定表述]
- 北极星: [效率、精确、可执行]
```

### 核心模块

| 模块 | 职责 |
|------|------|
| `src/detector.py` | 检测文本中的 MBTI 类型 |
| `src/loader.py` | 加载预设文件 |
| `src/memory.py` | 持久化用户偏好 |
| `skills/*.md` | MBTI 预设内容 |

---

## 使用方式

1. Claude Code 加载项目时读取 `CLAUDE.md`
2. 用户说出 MBTI 类型（如 `infp`）
3. AI 从 `skills/mbti-infp.md` 加载预设
4. 切换对话风格

---

## 技术约束

- **预设格式**: Markdown，纯文本
- **记忆存储**: JSON 文件
- **无外部依赖**: Phase 1 保持轻量
- **Python 版本**: 3.10+

---

## 成功标准

1. 用户说 `infp` → AI 用 INFP 风格对话
2. 用户说 `intj` → AI 用 INTJ 风格对话
3. 随时可以切换，不限次数
4. 可添加更多 MBTI 类型

---

## 待 Phase 2

- 更多 MBTI 预设（ENTJ、ESTJ、INTP 等）
- 架构层的真实多 Agent 对抗
- 记忆层的 RAG 向量检索
