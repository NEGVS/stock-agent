from app.state import StockState

#  第11步：Summary Agent（总控）
def summary_agent(state: StockState):
    stock = state['stock']
    decision = '观望'

    if state['risk']['level'] == 'LOW' and state['technical']['trend'] == '上涨':
        decision = '轻仓买入'
    if state['risk']['level'] == 'HIGH':
        decision = '禁止交易'

    state['summary'] = {
        'stock': stock,
        'decision': decision
    }

    state['messages'].append('Summary完成')
    return state
