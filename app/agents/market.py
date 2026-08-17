from app.state import StockState

from app.tools.stock_tool import get_stock_info

"""
第6步：把 Tool 接入 Node
创建一个新的 Node：

LLM
  ↓
决定要不要查数据
  ↓
调用 Tool
  ↓
返回结构化数据
"""
def market_node(state: StockState):
    stock = state["stock"]

    print(f"获取市场数据 for: {stock}")

    data = get_stock_info(stock)

    state["market_data"] = data

    state["status"] = "DONE_MARKET"
    print(f"返回 state : {state}")
    print(f"market_node 返回state: {state}")

    return state
