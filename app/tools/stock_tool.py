"""AKShare 行情数据采集。

把"取数"和"解析"拆开：
    fetch_spot_snapshot()  —— 只负责拿全市场快照，带重试
    get_stock_info()       —— 只负责把 DataFrame 行转成结构化 dict
节点只需调用后者，网络失败时拿到的是 {"found": False, ...} 而不是异常。
"""
import akshare as ak

from app.utils.network import setup_proxy

# akshare 会在 import 时读环境变量建立连接池，这里先确保代理配置生效
setup_proxy()

# 东方财富接口偶发抽风，重试能挡掉大部分瞬时失败
_MAX_RETRY = 3

_FAILED = {
    "found": False,
    "message": "未找到股票",
}

# 单只股票详情接口的字段映射：akshare 列名 → 我们对外暴露的 key
_FIELD_MAP = {
    "名称": "name",
    "代码": "code",
    "最新": "price",
    "涨跌额": "change",
    "涨跌幅": "change_pct",
    "成交量": "volume",
    "成交额": "amount",
    "总市值": "market_cap",
    "市盈率-动态": "pe",
}


def fetch_spot_snapshot():
    """拉取沪深京 A 股全市场实时快照。

    :return: DataFrame；全部重试失败时返回 None
    """
    last_error = None

    for attempt in range(1, _MAX_RETRY + 1):
        try:
            return ak.stock_zh_a_spot_em()
        except Exception as exc:  # 网络/接口异常都吞掉，交给调用方判断
            last_error = exc
            print(f"[stock_tool] 第 {attempt}/{_MAX_RETRY} 次拉取行情失败：{exc}")

    print(f"[stock_tool] 行情拉取最终失败：{last_error}")

    return None


def _row_to_dict(row) -> dict:
    data = {"found": True}

    for source, target in _FIELD_MAP.items():
        if source in row.index:
            data[target] = row[source]

    return data


def get_stock_info(stock_name: str) -> dict:
    """根据股票名称获取基础行情数据。

    :param stock_name: 股票名称，如 "信维通信"
    :return: 结构化行情；任何失败都返回 {"found": False, ...}，不抛异常
    """
    if not stock_name:
        return {"found": False, "message": "股票名称为空"}

    # 优先走单只股票详情接口：一次只拿一行，比拉全市场快两个数量级
    try:
        df = ak.stock_individual_info_em(symbol=stock_name)
    except Exception:
        df = None

    if df is not None and not df.empty:
        info = dict(zip(df["item"], df["value"]))
        if info.get("股票代码"):
            return {
                "found": True,
                "name": info.get("股票简称", stock_name),
                "code": info["股票代码"],
                "market_cap": info.get("总市值"),
                "industry": info.get("行业"),
                "price": _latest_price(info["股票代码"]),
            }

    # 兜底：全市场快照里按名称过滤
    snapshot = fetch_spot_snapshot()

    if snapshot is None:
        return {"found": False, "message": "行情接口不可用，请检查网络或代理配置"}

    result = snapshot[snapshot["名称"] == stock_name]

    if result.empty:
        return _FAILED

    return _row_to_dict(result.iloc[0])


def _latest_price(code: str):
    """取最新价。详情接口不带实时价，需要单独查一次。

    :param code: 6 位股票代码，如 "300136"
    """
    try:
        quote = ak.stock_bid_ask_em(symbol=code)
        row = quote[quote["item"] == "最新"]
        return float(row["value"].iloc[0]) if not row.empty else None
    except Exception:
        return None
