# TailoredBunny MBTI Skill

## 这是什么

TailoredBunny 让 AI 拥有 MBTI 人格。你可以选择 AI 的对话风格，AI 会记住你的偏好并不断进化。

---

## 使用方法

### 1. 切换模式

说出任意 MBTI 类型，AI 立即切换风格：

```
用户: intj
AI:   已切换到 INTJ 模式

用户: infp
AI:   已切换到 INFP 模式
```

**支持的所有类型：**
INTJ, INFP, INTP, INFJ, ISTJ, ISFJ, ISTP, ISFP, ENTJ, ENTP, ENFJ, ENFP, ESTJ, ESTP, ESFJ, ESFP

### 2. 反馈进化

当你给反馈时，AI 会记住你的偏好：

```
用户: entj
AI:   已切换到 ENTJ 模式

用户: 你太直接了，我需要更委婉一点
AI:   收到，已更新你的 ENTJ 偏好

用户: entj
AI:   已切换到 ENTJ 模式（使用你的私人进化版）
```

---

## 工作原理

### 文件结构

```
skills/
  mbti-*.md           # 通用 baseline（所有用户相同）
memory/
  customized-*.md      # 你的私人进化版（仅本地，不上传 git）
```

### 加载流程

当你说 MBTI 类型时：
1. 读取 `skills/mbti-{type}.md`（baseline）
2. 读取 `memory/customized-{type}.md`（你的私人部分，如果存在）
3. 两者合并 = 完整的风格

### 反馈流程

当你说"太X"或"需要更X"时：
1. 理解反馈内容
2. 检查 `memory/customized-{type}.md` 是否存在
3. 如果不存在，创建文件
4. 在"你的私人调整"下追加新条目
5. 告诉用户更新了什么

### 个性化文件

`memory/customized-*.md` 不会被上传到 git（已在 .gitignore 中）。
每个人有自己独立的进化版本，只保存在本地。

---

## 反馈格式

文件内容：
```markdown
# {MBTI} 进化版 - 你的私人部分

## 你的私人调整

- （日期）反馈内容
```

---

## 例子

```
用户: intj
AI:   已切换到 INTJ 模式

用户: 你太啰嗦了，我喜欢简洁
AI:   收到，已更新你的 INTJ 偏好

用户: infp
AI:   已切换到 INFP 模式

用户: 可以更温柔一点吗
AI:   收到，已更新你的 INFP 偏好

用户: intj
AI:   已切换到 INTJ 模式（baseline + 你的私人调整：喜欢简洁）
```
