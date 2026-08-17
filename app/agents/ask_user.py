from app.state import StockState

# 3- 第4步：新增一个 Node（AskUser）
def ask_user(state: StockState):
    print("未识别到股票，请补充名称")
    state["status"] = "WAIT_USER"
    print(f"ask_user返回state: {state}")

    return state
