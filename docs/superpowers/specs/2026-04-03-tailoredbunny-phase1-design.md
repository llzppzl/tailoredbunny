# TailoredBunny Phase 1 设计文档

> **状态**: 已批准
> **日期**: 2026-04-04
> **更新说明**: 已按实际需求更新（skill-based MBTI 切换 + 进化机制）

## 概述

TailoredBunny 是一个让 AI Agent 拥有"性格"的项目。像切换 superpowers skill 一样，随时切换 MBTI 人格模式，并且在日常交互中不断进化，越来越贴近用户期待的"性格"。

**Phase 1 目标**:
1. 实现 MBTI 模式切换 —— 用户说 `infp` 或 `intj`，AI 立即切换对话风格
2. 实现进化机制 —— baseline + customized 合并，通过反馈不断调整

---

## 核心流程

```
用户: intj
    ↓
AI 加载 skills/mbti-intj.md（baseline）
    ↓
AI 加载 memory/customized-intj.md（你的私人部分）
    ↓
两者合并 = 完整的 INTJ 风格
    ↓
用户给反馈（"太啰嗦了"）
    ↓
AI 更新 memory/customized-intj.md
    ↓
下次加载，你的私人部分增强
```

---

## 文件结构

```
tailoredbunny/
├── skills/
│   ├── mbti-intj.md           # INTJ 通用 baseline
│   └── mbti-infp.md           # INFP 通用 baseline
├── memory/
│   ├── customized-intj.md     # INTJ 私人进化版
│   ├── customized-infp.md     # INFP 私人进化版
│   └── user-personality.json   # 用户人格记录
├── presets/
│   ├── intro-prompt.md        # 入口引导（备用）
│   ├── preset-intj-strategist.md
│   └── preset-infp-companion.md
├── src/
│   ├── detector.py             # MBTI 检测器
│   ├── loader.py               # 预设加载器
│   └── memory.py               # 记忆模块
├── tests/
├── docs/
├── CLAUDE.md                   # 项目说明（自动加载）
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 进化机制详解

### Baseline vs Customized

| 类型 | 文件 | 性质 | 变化 |
|------|------|------|------|
| Baseline | `skills/mbti-*.md` | 通用标准 | 不变 |
| Customized | `memory/customized-*.md` | 私人进化 | 随反馈累积 |

### 合并逻辑

加载顺序：
1. 加载 `skills/mbti-*.md`（baseline）
2. 加载 `memory/customized-*.md`（私人部分）
3. 两者**合并** = 完整的风格

如果 customized 为空，只有 baseline 起作用。

### 进化方式

**显式反馈**：你直接告诉 AI 调整（如"太啰嗦了"）
**隐式观察**：AI 观察你的回复模式（后续实现）

---

## 使用方式

1. Claude Code 加载项目时读取 `CLAUDE.md`
2. 用户说出 MBTI 类型（如 `infp`）
3. AI 加载 `skills/mbti-infp.md` + `memory/customized-infp.md`
4. 两者合并后切换对话风格
5. 用户给反馈，AI 更新 customized

---

## MBTI 预设内容

### INTJ - 冷酷幕僚长

**风格**：直接给结论、不废话、MECE 表格、风险评估

**交互层**：N型（底层逻辑）、T型（冷酷逻辑）、I型（直接给结论）
**架构层**：J型（瀑布流）、红蓝对抗
**记忆层**：雷区、北极星

### INFP - 知心搭档

**风格**：先肯定情绪、再给建议、温和、支持

**交互层**：N型（愿景）、F型（情绪价值）、E型（允许讨论）
**架构层**：P型（敏捷迭代）、微步前进
**记忆层**：雷区、北极星

---

## 技术约束

- **预设格式**: Markdown，纯文本
- **记忆存储**: JSON 文件 + Markdown
- **无外部依赖**: Phase 1 保持轻量
- **Python 版本**: 3.10+

---

## 成功标准

1. 用户说 `infp` → AI 用 INFP 风格对话
2. 用户说 `intj` → AI 用 INTJ 风格对话
3. 随时可以切换，不限次数
4. 反馈自动更新 customized 文件
5. 下次加载时进化效果保留
6. 可添加更多 MBTI 类型

---

## 待 Phase 2

- 更多 MBTI 预设（ENTJ、ESTJ、INTP 等）
- 隐式观察（AI 自动分析用户回复模式）
- 架构层的真实多 Agent 对抗
- 记忆层的 RAG 向量检索
