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



# 2026-09

我刚刚是运行了main.py
这是输出的信息，请分析一下程序的执行逻辑 步骤，以及出现的问题

1-StateGraph
2-add_node
3-route_after_planner
Planner Start Working...
Planner 分析问题：分析信维通信
planner返回 state : {'question': '分析信维通信', 'stock': '信维通信', 'status': 'OK'}
route_after_planner 返回state: {'question': '分析信维通信', 'stock': '信维通信', 'status': 'OK'}
获取市场数据 for: 信维通信
Traceback (most recent call last):
  File "/Users/andy_mac/PycharmProjects/stock-agent/.venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 788, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/andy_mac/PycharmProjects/stock-agent/.venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 534, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
