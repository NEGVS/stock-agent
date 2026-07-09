from app.state import StockState

# 写第一个node
def planner(state: StockState):
    print('Planner Start Working...')
    state['stock'] = '信维通信'
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