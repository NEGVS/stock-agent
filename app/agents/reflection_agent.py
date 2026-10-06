from app.state import StockState


# 第4步：Reflection Agent 设计思想
# 它做三件事：
# 1. 对比预测 vs 结果
# 2. 找出错误原因
# 3. 给出修正策略

def reflection_agent(state: StockState):
    print('reflection_agent-1')

    print('开发反思本次决策')
    risk = state['risk']
    technical = state['technical']
    decision = state['summary']['decision']

    insights = []

    # ===规则1：高风险但买入
    if risk['level'] == 'HIGH' and decision == '轻仓买入':
        insights.append('风险过高仍然尝试买入，策略过于激进')
    # ===规则2：趋势错误
    if technical['trend'] == '下跌' and decision == '轻仓买入':
        insights.append('趋势操作风险较高')
    # ===规则3：超买信号
    if technical['rsi'] > 70:
        insights.append('RSI超买区域可能回调')

    if not insights:
        insights.append('本次决策逻辑稳定')
    state['reflection'] = {
        'insights': insights,
        'score': 'improve' if len(insights) > 1 else 'stable'
    }
    print('reflection_agent-2')

    return state
