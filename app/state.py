from typing import NotRequired, TypedDict


# 整个 Graph 的共享内存。
# Dictionary 比对象快。
# TypedDict 又有类型提示。
#
# total=False：所有字段都可缺省。
# 图是一步步往下走的——planner 阶段还没有 market_data，
# market 阶段还没有 summary，写成必填只会让类型检查失真。
# 每个节点只返回自己负责的字段，LangGraph 会做增量合并。
class StockState(TypedDict, total=False):
    # 输入
    question: str
    stock: NotRequired[str | None]  # 未识别到股票时为 None

    # 各节点的产出
    market_data: NotRequired[dict]
    news: NotRequired[str]
    technical: NotRequired[str]
    fund: NotRequired[str]
    risk: NotRequired[str]
    summary: NotRequired[str]

    # 流程控制
    status: NotRequired[str]
