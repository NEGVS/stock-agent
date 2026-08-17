from app.state import StockState


# 3- 第5步：新增 Technical Node
def technical(state: StockState):
    stock = state["stock"]
    print(f" 技术分析：{stock}")
    state["status"] = "DONE_TECH"
    print(f"返回 state : {state}")
    print(f"technical 返回state: {state}")

    return state
