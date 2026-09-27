"""AKShare 行情数据采集。

把"取数"和"解析"拆开：
    fetch_spot_snapshot()  —— 只负责拿全市场快照，多数据源自动降级
    get_stock_info()       —— 只负责把 DataFrame 行转成结构化 dict
节点只需调用后者，网络失败时拿到的是 {"found": False, ...} 而不是异常。

代理与封控补丁的初始化在 app/utils/bootstrap.py，
由 app/__init__.py 保证早于 `import akshare` 执行。

数据源选择（实测于 2026-09-27）：
    东方财富 push2 的 /api/qt/clist/get 在部分网络环境下会被阻断，
    先前一直降级到新浪源。装上 akshare_proxy_patch 后东财恢复可用，
    因此恢复"东财优先"——它比新浪快一倍且字段更全。
    新浪仍作为兜底保留：补丁未配置 token 或网关不可用时还能出数。

字段单位差异（重要，别踩）：
    东财"成交量"单位是手，新浪是股，相差 100 倍。
    这里按东财口径统一为「手」——即新浪源的 volume 会除以 100 后输出，
    并附带 volume_unit 字段标注，下游取用时不必再猜。
"""
import time

import akshare as ak

# 接口偶发抽风，重试能挡掉大部分瞬时失败
_MAX_RETRY = 3

# 快照缓存：东财源首次要 16~18s（多线程分页拉取），
# 同一轮分析里多个节点都要行情，不缓存会被反复拉。
_CACHE_TTL = 60  # 秒
_cache: dict = {"at": 0.0, "snapshot": None, "field_map": None}

# 记住哪个源失败过，避免每次调用都在坏源上白等重试
# 实测东财不通时，3 次重试要浪费 9s
_dead_sources: set = set()

# 新浪源的成交量单位是「股」，东财是「手」，统一到东财口径
_SINA_VOLUME_DIVISOR = 100

# 东方财富列名 → 对外统一 key
_EM_FIELD_MAP = {
    "名称": "name",
    "代码": "code",
    "最新价": "price",
    "涨跌额": "change",
    "涨跌幅": "change_pct",
    "成交量": "volume",
    "成交额": "amount",
    "今开": "open",
    "最高": "high",
    "最低": "low",
    "昨收": "prev_close",
}

# 新浪列名 → 对外统一 key（名称/代码用同一套 key，其余对应关系不同）
_SINA_FIELD_MAP = {
    "名称": "name",
    "代码": "code",
    "最新价": "price",
    "涨跌额": "change",
    "涨跌幅": "change_pct",
    "成交量": "volume",
    "成交额": "amount",
    "今开": "open",
    "最高": "high",
    "最低": "low",
    "昨收": "prev_close",
    "买入": "bid",
    "卖出": "ask",
}


def _fetch_eastmoney():
    """东方财富源：一次拿全市场快照。"""
    return ak.stock_zh_a_spot_em()


def _fetch_sina():
    """新浪源：一次拿全市场快照。

    比东财慢（内部分页拉取），但东财被封控时它往往还活着，留作兜底。
    代码列带 sh/sz 前缀，成交量单位是股，都需要归一化。
    """
    return ak.stock_zh_a_spot()


# (源名称, 取数函数, 字段映射, 成交量除数)，按顺序降级
# 成交量除数用于把各源统一到「手」：东财本来就是手，除数为 1
_SOURCES = (
    ("eastmoney", _fetch_eastmoney, _EM_FIELD_MAP, 1),
    ("sina", _fetch_sina, _SINA_FIELD_MAP, _SINA_VOLUME_DIVISOR),
)


def _normalize_code(code: str) -> str:
    """统一股票代码格式为 6 位数字。

    新浪返回 "sz300136"，东财返回 "300136"，对外只暴露 6 位。
    """
    code = str(code)
    for prefix in ("sh", "sz", "bj"):
        if code.startswith(prefix):
            return code[len(prefix):]

    return code


def fetch_spot_snapshot():
    """按优先级依次尝试各数据源拉取全市场快照。

    带缓存：TTL 内直接返回上次结果，避免同一轮分析反复拉取。

    :return: (DataFrame, 字段映射, 成交量除数) 三元组；全失败时返回 (None, None, None)
    """
    now = time.time()

    if _cache["snapshot"] is not None and now - _cache["at"] < _CACHE_TTL:
        return _cache["snapshot"], _cache["field_map"], _cache["divisor"]

    errors = []

    for name, fetch, field_map, divisor in _SOURCES:
        if name in _dead_sources:
            continue

        for attempt in range(1, _MAX_RETRY + 1):
            try:
                df = fetch()
                if df is not None and not df.empty:
                    _cache.update(
                        {"at": now, "snapshot": df, "field_map": field_map, "divisor": divisor}
                    )
                    if name != "eastmoney":
                        print(f"[stock_tool] 已降级到 {name} 数据源")
                    return df, field_map, divisor
            except Exception as exc:
                errors.append(f"{name}#{attempt}: {exc}")

        # 整个源重试完都失败，标记为不可用，本次进程内不再尝试
        _dead_sources.add(name)
        print(f"[stock_tool] {name} 源不可用，本次进程内跳过")

    print(f"[stock_tool] 所有数据源均失败：{errors[-1] if errors else '未知错误'}")

    return None, None, None


def _to_native(value):
    """把 numpy 标量转成 Python 原生类型。

    pandas 取出来的 np.float64 / np.int64 不能直接 JSON 序列化，
    也容易在接 LLM 或写日志时踩坑，这里统一转换。
    """
    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, AttributeError):
            return value

    return value


def _row_to_dict(row, field_map: dict, divisor: int = 1) -> dict:
    data = {"found": True}

    for source, target in field_map.items():
        if source in row.index:
            data[target] = _to_native(row[source])

    if "code" in data:
        data["code"] = _normalize_code(data["code"])

    # 统一成交量到「手」。各源单位不同（东财=手，新浪=股），
    # 不统一的话下游算指标会差 100 倍。
    if "volume" in data and divisor != 1 and data["volume"] is not None:
        data["volume"] = round(data["volume"] / divisor, 2)

    data["volume_unit"] = "手"

    return data


def get_stock_info(stock_name: str) -> dict:
    """根据股票名称获取基础行情数据。

    :param stock_name: 股票名称，如 "信维通信"
    :return: 结构化行情；任何失败都返回 {"found": False, ...}，不抛异常
    """
    if not stock_name:
        return {"found": False, "message": "股票名称为空"}

    snapshot, field_map, divisor = fetch_spot_snapshot()

    if snapshot is None:
        return {"found": False, "message": "所有行情数据源均不可用，请检查网络或代理配置"}

    result = snapshot[snapshot["名称"] == stock_name]

    if result.empty:
        return {"found": False, "message": f"未找到股票：{stock_name}"}

    return _row_to_dict(result.iloc[0], field_map, divisor)
