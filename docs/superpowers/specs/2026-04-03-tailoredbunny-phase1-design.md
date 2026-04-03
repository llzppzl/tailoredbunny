# TailoredBunny Phase 1 设计文档

> **状态**: 已批准
> **日期**: 2026-04-03

## 概述

TailoredBunny 是一个让 AI Agent 拥有"性格"的项目。通过 MBTI 三层映射法则，从交互层、架构层、记忆层三个维度实现个人认知对齐，让 AI 告别千篇一律的通用回答。

**Phase 1 目标**: 实现引导式 MBTI 人格注入 —— AI 主动发问，用户只需回答类型，剩余全部自动完成。

---

## 核心流程

```
用户启动 AI（加载入口 Prompt）
    ↓
AI 发问："你是什么 MBTI？"
    ↓
用户回答："INTJ"
    ↓
人格检测器识别类型
    ↓
加载对应预设，注入到 System Prompt
    ↓
记忆模块保存到本地
    ↓
后续对话全部适配该人格模式
```

---

## 文件结构

```
tailoredbunny/
├── presets/
│   ├── intro-prompt.md          # 入口引导 Prompt（AI 启动时加载）
│   ├── preset-intj-strategist.md # INTJ 完整预设
│   └── preset-infp-companion.md  # INFP 完整预设
├── memory/
│   └── user-personality.json    # 用户人格记忆（自动生成）
├── src/
│   ├── detector.py              # MBTI 人格检测器
│   └── loader.py               # 预设加载器
├── mcp/
│   └── server.py                # MCP 服务器（实现自动注入）
├── tests/
├── docs/
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 组件设计

### 1. 入口 Prompt (`presets/intro-prompt.md`)

**职责**: AI 启动时加载，触发引导式提问

**内容**:
```
你是一个 MBTI 人格适配助手。
你的任务是：
1. 检查用户是否有指定 MBTI 类型（查看 memory/user-personality.json）
2. 如果没有，主动询问："你是什么 MBTI？（例如：INTJ、INFP、ENTJ 等）"
3. 用户回答后，调用 loader 加载对应预设
4. 加载完成后，切换到该人格模式开始对话
```

### 2. 预设文件 (`presets/preset-{mbti}-{nickname}.md`)

**职责**: 定义每种 MBTI 类型的交互风格、架构层配置、记忆层配置

**INTJ 预设结构**:
```markdown
# INTJ - 冷酷幕僚长

## 交互层
- S/N: N型（要底层逻辑、战略视角）
- T/F: T型（冷酷逻辑、直击痛点）
- E/I: I型（直接给结论、减少确认）
- 输出格式: MECE 表格 + 风险评估

## 架构层
- J/P: J型（瀑布流、WBS、节点验收）
- 红蓝对抗: 开启
  - Agent A: 策划者，输出方案
  - Agent B: 批评者，找漏洞

## 记忆层
- 雷区: [避免废话、避免不确定表述]
- 北极星: [效率、精确、可执行]
```

**INFP 预设结构**:
```markdown
# INFP - 知心搭档

## 交互层
- S/N: N型（要愿景、可能性）
- T/F: F型（情绪价值、理解包容）
- E/I: E型（允许讨论、主动提问澄清）
- 输出格式: 先肯定情绪，再给建议，微步拆解

## 架构层
- J/P: P型（敏捷迭代、灵活调整）
- 微步前进: 开启
  - 每次只给一个极小任务
  - 强调"今天只做这一件"

## 记忆层
- 雷区: [避免高压指令、避免否定情绪]
- 北极星: [自我接纳、渐进成长]
```

### 3. 人格检测器 (`src/detector.py`)

**职责**: 解析用户输入，识别 MBTI 类型

**逻辑**:
- 接收用户文本输入（如 "INTJ"、"我是 INTJ"、"intj"）
- 提取 MBTI 类型字符串
- 验证格式（4个字母，E/I, S/N, T/F, J/P 各一个）
- 返回标准化的 MBTI 类型

**函数签名**:
```python
def detect_mbti(user_input: str) -> str | None:
    """
    解析用户输入，识别 MBTI 类型
    返回: "INTJ" | "INFP" | None（无法识别）
    """
```

### 4. 预设加载器 (`src/loader.py`)

**职责**: 根据 MBTI 类型加载对应预设文件

**逻辑**:
- 接收 MBTI 类型（如 "INTJ"）
- 查找 `presets/preset-intj-*.md` 文件
- 读取文件内容，返回完整预设文本

**函数签名**:
```python
def load_preset(mbti: str) -> str | None:
    """
    加载对应 MBTI 的预设
    返回: 预设文件内容 | None（预设不存在）
    """
```

### 5. 记忆模块 (`memory/user-personality.json`)

**职责**: 持久化保存用户人格类型，避免每次重复引导

**文件格式**:
```json
{
  "user_id": "default",
  "mbti": "INTJ",
  "updated_at": "2026-04-03T12:00:00Z"
}
```

### 6. MCP 服务器 (`mcp/server.py`)

**职责**: 通过 MCP 协议对接 AI 平台，实现自动注入

**功能**:
| 功能 | 说明 |
|------|------|
| 连接 AI | 通过 MCP 协议对接 Claude/GPT |
| 加载预设 | 读取 presets/*.md，转为 System Prompt |
| 管理记忆 | 读写 memory/user-personality.json |
| 触发引导 | 当无记忆时，通知 AI 发问 |

**接口**:
```python
# MCP 工具
def get_preset(mbti: str) -> str
def save_user_mbti(user_id: str, mbti: str) -> bool
def get_user_mbti(user_id: str) -> str | None
def detect_mbti_from_text(text: str) -> str | None
```

---

## 技术约束

- **预设文件格式**: Markdown，纯文本，无需解析器
- **记忆存储**: JSON 文件，轻量，无需数据库
- **MCP 协议**: 使用官方 Python SDK
- **Python 版本**: 3.10+
- **无外部依赖**（除 MCP SDK）：Phase 1 保持轻量

---

## 成功标准

1. 用户启动 AI，加载 intro-prompt.md，AI 自动问"你是什么 MBTI"
2. 用户回答 "INTJ"，AI 正确识别并加载 preset-intj-strategist.md
3. 后续对话全部以 INTJ 风格输出（MECE 表格、冷酷逻辑、无废话）
4. 再次启动 AI，AI 直接使用 INTJ 模式，不再重复提问
5. INFP 预设同样工作正常（情绪安抚、微步拆解）

---

## 待 Phase 2 实现

- 更多 MBTI 预设（ENTJ、ESTJ、INTP）
- 架构层的真实多 Agent 对抗（当前为模拟）
- 记忆层的 RAG 向量检索
- 完整 MCP 服务器功能
