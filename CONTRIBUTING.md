# Contributing to TailoredBunny

## 开发环境

```bash
# 克隆项目
git clone <repository-url>
cd tailoredbunny

# 安装依赖 (如有)
pip install -e .

# 运行测试
python -m pytest tests/ -v
```

## 添加新的 MBTI 预设

1. 在 `presets/` 目录创建新文件：`preset-{mbti}-{nickname}.md`
2. 参考现有预设格式定义交互层、架构层、记忆层
3. 添加测试用例

## 代码规范

- 使用 Python 3.10+
- 遵循 PEP 8
- 所有新功能需要测试
