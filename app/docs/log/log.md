# 如果你是 Conda 管 Python + uv 管依赖（你之前就是这个方案），直接：
uv add langgraph
uv add langchain
uv add langchain-openai
## 以后再装：
uv add akshare
uv add pandas
uv add pydantic

环境管理：Conda 管 Python 版本 + 全局环境隔离，UV 管项目依赖、极速安装
如何查安装了哪些包？
from langgraph.graph import StateGraph
这个导入报错



