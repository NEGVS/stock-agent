from app.state import StockState


#  第10步：Risk Agent（风控）
def risk_agent(state: StockState):
    risk_score = 0

    if state['technical']['rsi'] > 70:
        risk_score += 30

    if state['technical']['channge'] < 0:
        risk_score += 40
    state['risk'] = {
        'score': risk_score,
        'level': 'HIGH' if risk_score > 60 else 'LOW'
    }
    state['messages'].append('Risk分析完成')
    return state
