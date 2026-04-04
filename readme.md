# TailoredBunny

让 AI Agent 拥有"性格"的项目。像切换 skill 一样，随时切换 MBTI 人格模式，并且在日常交互中不断进化。

## 快速开始

### 1. 下载项目

```bash
git clone <repo-url>
cd tailoredbunny
```

### 2. 添加自定义指令

打开 Claude Code 设置 → 找到"自定义指令" → 添加以下内容：

```
当用户提到任何 MBTI 类型（INTJ, INFP, INTP, INFJ, ISTJ, ISFJ, ISTP, ISFP, ENTJ, ENTP, ENFJ, ENFP, ESTJ, ESTP, ESFJ, ESFP）时：

1. 立即切换到对应模式
2. 从 skills/mbti-{type}.md 加载 baseline
3. 从 memory/customized-{type}.md 加载私人偏好（如果存在）
4. 两者合并使用

当用户给反馈（如"太啰嗦了"、"需要更委婉"）时：
1. 在 memory/customized-{type}.md 的"你的私人调整"下追加新条目
2. 如果文件不存在，先创建
3. 告诉用户已更新
```

### 3. 开始使用

在 Claude Code 里进入 tailoredbunny 项目，然后：

```
你: intj
AI: 已切换到 INTJ 模式

你: entj
AI: 已切换到 ENTJ 模式

你: 太直接了，我需要更委婉
AI: 收到，已更新你的 ENTJ 偏好
```

---

## 工作原理

### 文件结构

| 文件 | 用途 |
|------|------|
| `skills/mbti-*.md` | 通用 baseline（不变） |
| `memory/customized-*.md` | 你的私人进化版（本地，不上传 git） |

### 进化流程

1. 你说 MBTI 类型 → AI 加载 baseline + 你的私人调整
2. 你给反馈 → AI 更新 customized 文件
3. 下次加载时，你的私人偏好会生效

---

## 支持的 MBTI 类型

| 类型 | 名称 | 特点 |
|------|------|------|
| INTJ | 冷酷幕僚长 | 直接给结论、MECE表格 |
| INFP | 知心搭档 | 温和、支持、每次一点点 |
| INTP | 逻辑学家 | 抽象分析、逻辑优先 |
| INFJ | 提倡者 | 理想主义、洞察人心 |
| ISTJ | 物流师 | 务实可靠、注重细节 |
| ISFJ | 守卫者 | 温暖忠诚、默默付出 |
| ISTP | 鉴赏家 | 灵活务实、善于动手 |
| ISFP | 探险家 | 温和敏感、热爱自由 |
| ENTJ | 指挥官 | 果断自信、战略思维 |
| ENTP | 辩论家 | 聪明好奇、爱辩论 |
| ENFJ | 主人公 | 热情感染、激励人心 |
| ENFP | 竞选者 | 创意活力、充满可能 |
| ESTJ | 总经理 | 务实果断、执行力强 |
| ESTP | 企业家 | 活力行动、灵活应变 |
| ESFJ | 供给者 | 热情友好、照顾他人 |
| ESFP | 表演者 | 活泼开朗、享受当下 |
