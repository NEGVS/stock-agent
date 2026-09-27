from app.state import StockState


# 3- 第4步：新增一个 Node（AskUser）
def ask_user(state: StockState):
    message = "未识别到股票，请补充名称"
    print(message)

    return {"summary": message, "status": "WAIT_USER"}
