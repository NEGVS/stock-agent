
from app.state import StockState

from app.tools.indicator import (
    generate_mock_kline,
    calc_ma, calc_rsi
)

# 技术分析 Agent,Technical Node（核心）
# 3- 第5步：新增 Technical Node
def technical(state: StockState):
    stock = state.get("stock")

    print(f" 技术分析：{state['stock']}")

    df = generate_mock_kline()

    ma5 = calc_ma(df, 5)
    ma20 = calc_ma(df, 20)
    rsi = calc_rsi(df)

    # ===趋势判断===
    if ma5 > ma20:
        trend = "上涨趋势"
    else:
        trend = "下跌/震荡"

    # ==rsi判断==
    if rsi > 70:
        signal = "超买（谨慎）"
    elif rsi > 30:
        signal = "超卖（机会）"
    else:
        signal = "中性"

    state["technical"] = {
        "ma5": ma5,
        "ma20": ma20,
        "rsi": rsi,
        "trend": trend,
        "signal": signal
    }

    state["status"] = "DONE_TECH"
    return state


#  第7步：Technical Agent（升级版）

def technical_agent(state: StockState):
    df = generate_mock_kline()
    print('technical_agent-1')

    ma5 = calc_ma(df, 5)
    ma20 = calc_ma(df, 20)
    rsi = calc_rsi(df)

    trend = '上涨' if ma5 > ma20 else '下跌'

    state['technical'] = {
        "ma5": ma5,
        "ma20": ma20,
        "rsi": rsi,
        "trend": trend
    }

    state['messages'].append('Technical 分析完成')
    print('technical_agent-2')

    return state