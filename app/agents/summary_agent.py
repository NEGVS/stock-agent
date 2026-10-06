from app.state import StockState
from app.memory.memory import save_memory


#  第11步：Summary Agent（总控）
def summary_agent(state: StockState):
    stock = state['stock']
    decision = state['summary']['decision']

    if state['risk']['level'] == 'LOW' and state['technical']['trend'] == '上涨':
        decision = '轻仓买入'
    if state['risk']['level'] == 'HIGH':
        decision = '禁止交易'

    state['summary'] = {
        'stock': stock,
        'decision': decision
    }

    state['messages'].append('Summary完成')
    # 保存经验，写入 Memory（总结后）
    save_memory(stock, {
        'last_decision': decision,
        'risk': state['risk'],
        'technical': state['technical'],
    })
    state['messages'].append('Memory已更新')

    return state
