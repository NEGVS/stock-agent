import pandas as pd


def generate_mock_kline():
    import numpy as np

    np.random.seed(42)

    price = 100

    data = []

    for i in range(50):
        price += np.random.randn()

        data.append(price)

    return pd.DataFrame({
        "close": data
    })

# 计算 MA（均线）
def calc_ma(df, window=5):

    return df["close"].rolling(window).mean().iloc[-1]


# 计算 RSI（简化版）

def calc_rsi(df, period=14):

    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return float(rsi.iloc[-1])