# TailoredBunny Phase 1 设计文档

> **状态**: 已批准
> **日期**: 2026-04-04
> **更新说明**: 已按实际需求更新（skill-based MBTI 切换 + 进化机制）

## 概述

TailoredBunny 是一个让 AI Agent 拥有"性格"的项目。像切换 superpowers skill 一样，随时切换 MBTI 人格模式，并且在日常交互中不断进化，越来越贴近用户期待的"性格"。

**Phase 1 目标**:
1. 实现 MBTI 模式切换 —— 用户说任意 MBTI 类型，AI 立即切换对话风格
2. 实现进化机制 —— baseline + customized 合并，通过反馈不断调整

---

## 核心流程

```
用户: entj
    ↓
AI 加载 skills/mbti-entj.md（baseline）
    ↓
AI 加载 memory/customized-entj.md（你的私人部分）
    ↓
两者合并 = 完整的 ENTJ 风格
    ↓
用户给反馈（"太直接了"）
    ↓
AI 更新 memory/customized-entj.md
    ↓
下次加载，你的私人部分增强
```

---

## 文件结构

```
tailoredbunny/
├── skills/
│   ├── mbti-intj.md           # INTJ 冷酷幕僚长
│   ├── mbti-infp.md           # INFP 知心搭档
│   ├── mbti-intp.md           # INTP 逻辑学家
│   ├── mbti-infj.md           # INFJ 提倡者
│   ├── mbti-istj.md           # ISTJ 物流师
│   ├── mbti-isfj.md           # ISFJ 守卫者
│   ├── mbti-istp.md           # ISTP 鉴赏家
│   ├── mbti-isfp.md           # ISFP 探险家
│   ├── mbti-entj.md           # ENTJ 指挥官
│   ├── mbti-entp.md           # ENTP 辩论家
│   ├── mbti-enfj.md           # ENFJ 主人公
│   ├── mbti-enfp.md           # ENFP 竞选者
│   ├── mbti-estj.md           # ESTJ 总经理
│   ├── mbti-estp.md           # ESTP 企业家
│   ├── mbti-esfj.md           # ESFJ 供给者
│   └── mbti-esfp.md           # ESFP 表演者
├── memory/
│   ├── customized-intj.md     # INTJ 私人进化版
│   ├── customized-infp.md     # INFP 私人进化版
│   └── customized-*.md         # 其他类型私人进化版
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
2. 用户说出 MBTI 类型（如 `entj`）
3. AI 加载 `skills/mbti-entj.md` + `memory/customized-entj.md`
4. 两者合并后切换对话风格
5. 用户给反馈，AI 更新 customized

---

## 技术约束

- **预设格式**: Markdown，纯文本
- **无代码依赖**: 完全基于文件操作
- **轻量**: 无外部依赖

---

## 成功标准

1. 用户说任意 MBTI 类型 → AI 用对应风格对话
2. 随时可以切换，不限次数
3. 反馈自动更新 customized 文件
4. 下次加载时进化效果保留

---

## 待 Phase 2

- 隐式观察（AI 自动分析用户回复模式）
- 进化算法优化
- 可视化进化过程
