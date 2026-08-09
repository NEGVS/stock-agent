# Conda + UV 正确使用指南

## 设计理念

- **Conda**：管理 Python 版本 + 全局环境隔离
- **UV**：管理项目依赖 + 极速安装

## 项目初始化

### 1. 创建 Conda 环境（指定 Python 版本）

```bash
conda create -n stock-agent python=3.11
conda activate stock-agent
```

### 2. 创建 UV 虚拟环境（使用 Conda 的 Python）

```bash
# 在项目根目录
uv venv --python /opt/anaconda3/envs/stock-agent/bin/python
```

这会创建 `.venv` 目录，使用 Conda 环境的 Python，但由 UV 管理依赖。

### 3. 初始化项目配置

创建 `pyproject.toml`：

```toml
[project]
name = "stock-agent"
version = "0.1.0"
description = "AI-powered stock analysis system"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "langgraph>=1.2.8",
    "python-dotenv>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["app"]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

## 日常开发工作流

### 方法1：使用 `uv run`（推荐）

**优点：** 自动使用正确的虚拟环境，无需手动激活

```bash
# 运行 Python 脚本
uv run python main.py

# 运行 Python 命令
uv run python -c "from langgraph.graph import StateGraph"

# 运行测试
uv run pytest

# 运行格式化
uv run black .
```

### 方法2：手动激活 .venv

**注意：** 必须先退出 Conda 环境！

```bash
# 1. 退出 Conda 环境
conda deactivate

# 2. 激活 UV 创建的 .venv
source .venv/bin/activate

# 3. 现在可以直接使用 python
python main.py
from langgraph.graph import StateGraph  # 可用
```

**常见错误：** 如果不先 `conda deactivate`，即使 `source .venv/bin/activate` 后，Python 仍会指向 Conda 环境。

## 依赖管理

### 添加依赖

```bash
# 添加生产依赖
uv add langgraph
uv add requests

# 添加开发依赖
uv add --dev pytest
uv add --dev black
```

### 移除依赖

```bash
uv remove package-name
```

### 同步依赖（安装所有依赖）

```bash
uv sync
```

### 查看已安装的包

```bash
uv pip list
```

## IDE 配置（PyCharm）

### 配置 Python 解释器

1. **PyCharm → Settings/Preferences**
2. **Project: stock-agent → Python Interpreter**
3. 点击**齿轮图标** → **Add Interpreter** → **Add Local Interpreter**
4. 选择 **Existing**
5. 路径填写：`/Users/andy_mac/PycharmProjects/xai/stock-agent/.venv/bin/python`
6. 点击 OK

配置完成后，PyCharm 会自动使用 `.venv` 环境，所有导入和代码提示都能正常工作。

## 验证环境配置

### 检查 Python 路径

```bash
# 方法1：使用 uv run
uv run python -c "import sys; print('Python:', sys.executable)"
# 期望输出：.../stock-agent/.venv/bin/python

# 方法2：激活 .venv 后
conda deactivate
source .venv/bin/activate
which python
# 期望输出：.../stock-agent/.venv/bin/python
```

### 测试导入

```bash
uv run python -c "from langgraph.graph import StateGraph; print('✅ Import successful')"
```

## 常见问题排查

### 问题1：`ModuleNotFoundError: No module named 'langgraph'`

**原因：** 当前使用的是 Conda 环境，而不是 .venv

**解决：**
```bash
# 选项1：使用 uv run
uv run python your_script.py

# 选项2：正确激活 .venv
conda deactivate
source .venv/bin/activate
```

### 问题2：终端提示符显示两个环境名 `(stock-agent) (stock-agent)`

**原因：** Conda 环境和 .venv 同时激活了

**解决：**
```bash
conda deactivate  # 只保留 .venv
```

### 问题3：PyCharm 中导入报错

**原因：** PyCharm 使用的解释器不是 .venv

**解决：** 按照上面的"IDE 配置"部分配置 Python 解释器

## 项目结构

```
stock-agent/
├── .venv/                  # UV 创建的虚拟环境（使用 Conda 的 Python）
├── app/                    # 项目代码
│   ├── __init__.py
│   ├── agents/
│   ├── graph/
│   └── tools/
├── pyproject.toml          # 项目配置和依赖声明
├── uv.lock                 # 依赖锁定文件（自动生成）
├── README.md
├── .env.example            # 环境变量模板
└── .env                    # 实际环境变量（不提交到 git）
```

## 环境变量管理

### 创建 .env.example

```bash
# .env.example
DASHSCOPE_API_KEY=your_api_key_here
```

### 创建 .env（实际使用）

```bash
cp .env.example .env
# 编辑 .env，填入真实的 API Key
```

### 在代码中使用

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
```

## 安全规范

✅ **必须做到：**
- .env.example 提交到 git
- .env 永不提交（加入 .gitignore）
- 所有密钥使用 `os.getenv()` 读取
- 永远不要在代码中硬编码 API Key

❌ **永远不要做：**
- 写死 API Key
- 提交 .env 文件
- 在 commit log 中写入 key
- 复制生产环境的 key 到测试代码

## 总结

| 任务 | 命令 |
|------|------|
| 运行脚本 | `uv run python main.py` |
| 添加依赖 | `uv add package-name` |
| 移除依赖 | `uv remove package-name` |
| 同步依赖 | `uv sync` |
| 查看包列表 | `uv pip list` |
| 手动激活 | `conda deactivate && source .venv/bin/activate` |

**推荐工作流：** 使用 `uv run` 执行所有 Python 命令，无需手动管理环境激活。
