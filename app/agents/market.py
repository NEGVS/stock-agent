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

    if not stock:
        # 路由保证这里 stock 非空，但留个兜底：
        # 宁可带着"没数据"往下走，也不要让整张图崩掉
        print("[market] stock 为空，跳过行情查询")
        return {"market_data": {"found": False, "message": "股票名称为空"}, "status": "DONE_MARKET"}

    try:
        data = get_stock_info(stock)
    except Exception as exc:
        # 取数失败不是致命错误，标记后继续走 technical，
        # 让后续节点有机会降级处理（比如只做技术面分析）
        print(f"[market] 行情查询异常：{exc}")
        data = {"found": False, "message": f"行情查询失败：{exc}"}

    print(f"返回 state : {state}")
    print(f"market_node 返回state: {state}")

    return {"market_data": data, "status": "DONE_MARKET"}


#  第6步：Market Agent（升级版）
def market_agent(state: StockState):
    stock = state['stock']

    data = get_stock_info(stock)

    state['market_data'] = data

    state['messages'].append('Market分析完成')

    return state
