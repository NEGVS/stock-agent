from app.state import StockState
from app.memory.memory import load_memory


# 读取历史经验

def memory_agent(state: StockState):
    stock = state['stock']

    history = load_memory(stock)
    if history:
        print("读取记忆")
        state['memory'] = history

    else:
        print('无历史记忆')
        state['memory'] = {}
    return state
