import akshare as ak

# Tool 不是函数，它是： # Agent 的“外部能力”
def get_stock_info(stock_name: str):
    """
    根据股票名称获取基础行情数据
    :param stock_name:
    :return:
    """
    df = ak.stock_zh_a_spot_em()

    result = df[df["名称"] == stock_name]

    if result.empty:
        return {
            "found": False,
            "message": "未找到股票"
        }

    row = result.iloc[0]

    return {
        "found": True,
        "name": row["名称"],
        "code": row["代码"],
        "price": row["最新价"],
        "change": row["涨跌额"],
        "volume": row["成交量"]
        }