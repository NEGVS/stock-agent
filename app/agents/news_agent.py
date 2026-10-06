from app.state import StockState


# 第8步：News Agent（新增）
def news_agent(state: StockState):
    print('news_agent-1')

    stock = state['stock']

    # 模拟新闻，（后面接真是api）
    news = [
        f'{stock} 发布新产品',
        f'{stock} 机构调研增加'
    ]
    state['news'] = {
        'items': news,
        'sentiment': 'positive'
    }
    state['messages'].append('News分析完成')
    print('news_agent-2')

    return state
