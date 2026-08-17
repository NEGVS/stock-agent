from app.state import StockState

# Planner 不是“分析器”，而是：
# 决策 + 信息抽取器
# 它做的事情：
# 从 question → 提取 stock
# 并决定下一步状态

# 写第一个node
def planner(state: StockState):
    print('Planner Start Working...')
    question = state["question"]
    print(f"Planner 分析问题：{question}")

    if "信维" in question:
        state['stock'] = '信维通信'
        state['status'] = 'OK'
    else:
        state['stock'] = None
        state['status'] = 'NEED_INPUT'
    print(f"planner返回 state : {state}")

    return state
# node的本质
# 输入 State
# ↓
# 处理
# ↓
# 返回 State
# --------------
# 每个人都知道：
# 收到的是 State。
# 返回的也是 State。
# 所以不用关心前面是谁。
