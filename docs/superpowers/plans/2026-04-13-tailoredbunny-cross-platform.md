# TailoredBunny 跨平台 Skill 兼容改造实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 TailoredBunny 打造成支持 Claude MCP、代码框架（SK/LangChain）、SaaS 平台（Coze/Dify）、API 直连四种加载方式的跨平台 Skill 集。

**Architecture:** 保持现有 `skills/mbti-*.md` 为核心资产，为每个平台创建对应的适配层文件（config.json、manifest.yaml、mcp_server.py 等），实现"一份核心，多端适配"。

**Tech Stack:** Python 3.10+, FastMCP/mcp Python SDK, JSON Schema, YAML

---

## 文件结构（目标）

```
tailoredbunny/
├── skills/                              # 【核心资产】现有 16 个 MBTI prompt 文件
│   ├── mbti-intj.md
│   ├── mbti-infp.md
│   └── ... (共16个)
├── memory/                              # 【运行时生成】用户私人定制
│   └── customized-*.md
├── platform/                            # 【新建】各平台适配层
│   ├── claude/                         # Claude MCP 适配
│   │   ├── mcp_server.py              # 完整实现骨架
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── semantic-kernel/                # SK 框架适配
│   │   ├── intj/                       # 每个 MBTI 一个子文件夹
│   │   │   ├── prompt.md               # 【预处理】纯净 prompt
│   │   │   └── config.json            # SK 运行参数
│   │   ├── infp/
│   │   │   ├── prompt.md
│   │   │   └── config.json
│   │   └── ... (共16个)
│   ├── saas/                           # SaaS 平台适配
│   │   ├── IMPORT_GUIDE.md            # 【修改】手动导入指南
│   │   └── assets/                    # Logo 等资源
│   │       └── avatar.svg
│   └── api/                            # API 直连适配
│       └── prompts.yaml               # 统一索引配置
├── CLAUDE.md                           # 【现有】项目指令
├── readme.md                           # 【现有】主文档
└── docs/superpowers/plans/             # 【现有】计划目录
```

---

## 一、现状分析

### 1.1 当前项目拥有的文件

| 路径 | 类型 | 作用 |
|------|------|------|
| `skills/mbti-*.md` (16个) | 核心资产 | 各 MBTI 类型的 System Prompt baseline |
| `memory/customized-*.md` (4个) | 运行时生成 | 用户私人调整（不提交 git） |
| `CLAUDE.md` | 项目指令 | AI 加载规则（手动告知） |
| `readme.md` | 文档 | 人类可读说明 |

### 1.2 各平台缺失文件清单

| 平台 | 缺失文件 | 说明 |
|------|----------|------|
| **Claude MCP** | `platform/claude/mcp_server.py` | MCP Server wrapper，扫描 skills/ 并暴露为 prompts |
| **Claude MCP** | `platform/claude/requirements.txt` | MCP SDK 依赖 |
| **Claude MCP** | `platform/claude/README.md` | 安装配置指南 |
| **SK/LangChain** | `platform/semantic-kernel/*/skprompt.txt` | 每个 MBTI 一个副本（需预处理，16个） |
| **SK/LangChain** | `platform/semantic-kernel/*/config.json` | 每个 MBTI 一个配置（16个） |
| **SK/LangChain** | `platform/semantic-kernel/intj/prompt.md` | 【新增】SK 专用纯净 prompt 副本 |
| **SaaS (Coze/Dify)** | `platform/saas/IMPORT_GUIDE.md` | 【修改】导入指南（非 manifest） |
| **SaaS** | `platform/saas/assets/avatar.png` | 技能图标 |
| **API 直连** | `platform/api/prompts.yaml` | 统一索引配置 |

### 1.3 关键问题与解决方案

> ⚠️ **审查发现的问题**（已修复到任务分解中）：

1. **SK 文件不能直接复制** - `skills/mbti-*.md` 包含元指令（命令表、memory 引用、"当前模式"注释），需预处理提取纯净 prompt
2. **Coze/Dify 无统一 manifest 格式** - 改为提供 IMPORT_GUIDE.md 手动导入说明
3. **mcp_server.py 需要完整实现** - 提供可运行的代码骨架
4. **SK config.json 格式错误** - 改用 SK 官方标准格式

---

## 二、任务分解

### Task 1: 创建平台目录结构

**Files:**
- Create: `platform/claude/.gitkeep`
- Create: `platform/semantic-kernel/.gitkeep`
- Create: `platform/saas/assets/.gitkeep`
- Create: `platform/api/.gitkeep`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p platform/claude
mkdir -p platform/semantic-kernel
mkdir -p platform/saas/assets
mkdir -p platform/api
touch platform/claude/.gitkeep
touch platform/semantic-kernel/.gitkeep
touch platform/saas/assets/.gitkeep
touch platform/api/.gitkeep
```

- [ ] **Step 2: 验证目录创建**

Run: `ls -la platform/`
Expected: 显示 claude, semantic-kernel, saas, api 四个目录

---

### Task 2: 创建 Semantic Kernel 适配文件（16个 MBTI）

> ⚠️ **预处理要求**：`skills/mbti-*.md` 包含元指令（命令表、memory 引用、"当前模式"注释），不能直接复制。需提取纯净 prompt 内容。

**Files:**
- Create: `platform/semantic-kernel/intj/prompt.md`（SK 专用纯净副本）
- Create: `platform/semantic-kernel/intj/config.json`
- Create: `platform/semantic-kernel/infp/prompt.md`
- Create: `platform/semantic-kernel/infp/config.json`
- ... (共16组，32个文件)

- [ ] **Step 1: 为 INTJ 创建 SK 适配文件**

**1a. 创建 `platform/semantic-kernel/intj/prompt.md`**

从 `skills/mbti-intj.md` 提取**纯净 prompt 内容**：
- ✅ 保留：交互层、架构层、记忆层的内容
- ❌ 移除：命令表（`| intj | INTJ - ...`）、memory 引用注释、`## 当前模式`、文件头部的元信息

参考格式（纯净内容）：
```markdown
# INTJ - 逻辑学家

## 对 AI 的真实痛点
- AI 总是给模糊的、无法执行的建议
- AI 输出太理论，不看数据和历史

## 交互层
- S/N: N型（宏大愿景、底层逻辑、思维导图）
- T/F: T型（冷酷逻辑、直击痛点）
- E/I: I型（独立思考、不需要陪伴）
- 输出格式: 战略分析、风险评估、底层逻辑

## 架构层
- J/P: J型（高效执行、节点验收）
- 执行模式: 开启
  - 高效执行
  - 按节点跟踪
- 对拖延和借口零容忍

## 记忆层
- 雷区: [拖延、无组织、空洞理论]
- 北极星: [效率、责任、成功、执行力]
```

**1b. 创建 `platform/semantic-kernel/intj/config.json`**

```json
{
  "schema": 1.1,
  "description": "INTJ - 逻辑学家（战略幕僚）",
  "prompts": [
    {
      "description": "INTJ 性格适配 prompt",
      "template": "（从 prompt.md 读取内容）",
      "template_format": "semantic-kernel"
    }
  ],
  "execution_settings": {
    "default": {
      "max_tokens": 2000,
      "temperature": 0.7
    }
  }
}
```

- [ ] **Step 2: 为其他 15 个 MBTI 类型重复上述操作**

依次为：infp, intp, infj, istj, isfj, istp, isfp, entj, entp, enfj, enfp, estj, estp, esfj, esfp

> 注意：每个类型都要手动提取纯净内容，移除元指令

- [ ] **Step 3: 验证文件数量**

Run: `find platform/semantic-kernel -name "prompt.md" | wc -l` && `find platform/semantic-kernel -name "config.json" | wc -l`
Expected: 16 个 prompt.md 文件，16 个 config.json

---

### Task 3: 创建 SaaS 平台适配文件

> ⚠️ **重要说明**：Coze 和 Dify 没有统一的 manifest 导入格式。改为提供手动导入指南文档。

**Files:**
- Create: `platform/saas/IMPORT_GUIDE.md`（各平台导入说明）
- Create: `platform/saas/assets/avatar.svg` (占位图标)

- [ ] **Step 1: 创建 `platform/saas/IMPORT_GUIDE.md`**

```markdown
# TailoredBunny SaaS 平台导入指南

## Coze 平台导入

1. 打开 [Coze](https://www.coze.com) 并登录
2. 创建 Bot 或进入已有 Bot 编辑页面
3. 在"人设与回复逻辑"（System Prompt）框中，复制以下对应 MBTI 的内容

## Dify 平台导入

1. 打开 Dify 并登录
2. 创建 Agent 或进入已有 Agent 设置
3. 在"系统提示词"框中，复制以下对应 MBTI 的内容

## MBTI Prompt 内容索引

| MBTI | 文件位置 |
|------|----------|
| INTJ | `../../skills/mbti-intj.md` |
| INFP | `../../skills/mbti-infp.md` |
| ... | ... |

## 内容提取说明

由于 skills/ 目录下的文件包含元指令（命令表等），请使用以下**纯净版本**：

**INTJ 纯净版：**
（粘贴此处...）

**INFP 纯净版：**
（粘贴此处...）

... (其他14个 MBTI 同理)
```

- [ ] **Step 2: 创建占位 SVG 图标**

创建简单的 SVG 占位图 `platform/saas/assets/avatar.svg`

- [ ] **Step 3: 验证文件创建**

Run: `ls -la platform/saas/`
Expected: 显示 IMPORT_GUIDE.md 和 assets/ 目录

---

### Task 4: 创建 API 直连适配文件

**Files:**
- Create: `platform/api/prompts.yaml`

- [ ] **Step 1: 创建 prompts.yaml**

```yaml
# TailoredBunny API 提示词索引
version: "1.0"
prompts:
  - id: "mbti-intj"
    name: "INTJ - 逻辑学家"
    file: "../../skills/mbti-intj.md"
    variables: []
    description: "战略幕僚型，独立思考，擅长长期规划"
  - id: "mbti-infp"
    name: "INFP - 知心搭档"
    file: "../../skills/mbti-infp.md"
    variables: []
    description: "理想主义者，高共情，擅长情绪疏导"
  # ... 其他14个 MBTI 类型
```

- [ ] **Step 2: 验证 YAML 语法**

Run: `python -c "import yaml; yaml.safe_load(open('platform/api/prompts.yaml'))"`
Expected: 无错误

---

### Task 5: 创建 Claude MCP 适配文件

**Files:**
- Create: `platform/claude/mcp_server.py`
- Create: `platform/claude/requirements.txt`
- Create: `platform/claude/README.md`

- [ ] **Step 1: 创建 requirements.txt**

```
mcp>=1.0.0
fastmcp>=0.1.0
pyyaml>=6.0
```

- [ ] **Step 2: 创建 mcp_server.py**

> ⚠️ **完整实现骨架**（而非伪代码）

```python
"""
TailoredBunny MCP Server
为 Claude Code 提供 MBTI 性格适配 prompt

使用方法：
1. pip install -r requirements.txt
2. 配置 MCP Server（见 README.md）
3. 重启 Claude Code
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
            name=f"mbti-{p["type"].lower()}",
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
```

- [ ] **Step 3: 创建 README.md**

包含：
1. 安装依赖步骤
2. 使用 `claude mcp add` 命令添加 MCP Server
3. 重启 Claude Code 后使用 `/mbti-intj` 等命令触发

```markdown
# TailoredBunny MCP Server

## 安装步骤

1. 安装依赖：
   ```bash
   cd platform/claude
   pip install -r requirements.txt
   ```

2. 添加 MCP Server 到 Claude Code：


   **获取 mcp_server.py 绝对路径：**
   在文件管理器中右键 `platform/claude/mcp_server.py` → 复制文件路径

   **运行以下命令（请替换路径）：**
   ```bash
   # 用户级安装（所有项目可用）
   claude mcp add tailoredbunny -s user -- python 【mcp_server.py的绝对路径】

   # 或项目级安装（仅当前项目可用，可共享给团队）
   claude mcp add tailoredbunny -s project -- python 【mcp_server.py的绝对路径】
   ```

3. 重启 Claude Code（或关闭当前窗口后重新打开）

## 使用方式

在 Claude 输入框中：
- `/mbti-intj` - 切换到 INTJ 逻辑学家模式
- `/mbti-infp` - 切换到 INFP 知心搭档模式
- ... (其他 14 个 MBTI 同理)
```

---

### Task 6: 更新根目录文档

**Files:**
- Modify: `readme.md` - 新增"跨平台使用"章节
- Modify: `CLAUDE.md` - 可选，保持当前逻辑

- [ ] **Step 1: 更新 readme.md**

在快速开始后新增章节：
```markdown
## 跨平台使用

TailoredBunny 支持多种平台的 Skill 加载方式：

| 平台 | 使用方式 | 配置文件位置 |
|------|----------|--------------|
| Claude Code | 安装 MCP Server | `platform/claude/README.md` |
| Semantic Kernel | 指向 skill 目录 | `platform/semantic-kernel/` |
| Coze/Dify | 手动导入 | `platform/saas/IMPORT_GUIDE.md` |
| API 直连 | 读取 prompts.yaml | `platform/api/prompts.yaml` |
```

- [ ] **Step 2: 验证 readme.md 更新**

Run: `grep -c "platform/" readme.md`
Expected: > 0

---

## 三、验证与测试

### 3.1 文件完整性检查

- [ ] **检查 1: SK 文件数量**

Run: `find platform/semantic-kernel -name "config.json" | wc -l`
Expected: 16

- [ ] **检查 2: IMPORT_GUIDE.md 包含所有 16 个 MBTI**

Run: `grep -c "mbti-" platform/saas/IMPORT_GUIDE.md`
Expected: >= 16 (每个 MBTI 至少出现一次)

- [ ] **检查 3: prompts.yaml 索引完整**

Run: `grep -c "mbti-" platform/api/prompts.yaml`
Expected: 16

### 3.2 语法检查

- [ ] **检查 4: 所有 JSON 文件合法**

Run: `find platform/ -name "*.json" -exec python -c "import json; json.load(open('{}'))" \;`
Expected: 无错误

- [ ] **检查 5: 所有 YAML 文件合法**

Run: `find platform/ -name "*.yaml" -exec python -c "import yaml; yaml.safe_load(open('{}'))" \;`
Expected: 无错误

---

## 四、交付物清单

| 文件 | 数量 | 状态 |
|------|------|------|
| `platform/semantic-kernel/*/prompt.md` | 16 | 新建（需预处理提取） |
| `platform/semantic-kernel/*/config.json` | 16 | 新建 |
| `platform/saas/IMPORT_GUIDE.md` | 1 | 新建（替代 manifest） |
| `platform/saas/assets/avatar.svg` | 1 | 新建（占位） |
| `platform/api/prompts.yaml` | 1 | 新建 |
| `platform/claude/mcp_server.py` | 1 | 新建（完整骨架） |
| `platform/claude/requirements.txt` | 1 | 新建 |
| `platform/claude/README.md` | 1 | 新建 |
| `readme.md` | 1 | 更新 |

---

## 五、依赖关系

```
Task 1 (目录结构)
    ↓
Task 2 (SK 文件) ← 并行: Task 3, Task 4
Task 3 (SaaS 文件) ← 并行: Task 2, Task 4
Task 4 (API 文件) ← 并行: Task 2, Task 3
    ↓
Task 5 (Claude MCP) ← 依赖 Task 1 完成
    ↓
Task 6 (更新文档) ← 依赖所有任务完成
```
