from app.state import StockState


# 3- 第5步：新增 Technical Node
def technical(state: StockState):
    stock = state.get("stock")
    print(f" 技术分析：{stock}")

    market_data = state.get("market_data") or {}

    if not market_data.get("found"):
        print(f"[technical] 缺少行情数据：{market_data.get('message')}")

    return {"technical": f"{stock} 技术面分析占位", "status": "DONE_TECH"}
