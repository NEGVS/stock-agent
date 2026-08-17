from typing import TypedDict,Optional


# 整个 Graph 的共享内存。
# Dictionary 比对象快。
# TypedDict 又有类型提示。

class StockState(TypedDict):
    # 这就是所有节点共享的数据。
    question: str
    stock: Optional[str]
    news: str
    technical: str
    fund: str
    risk: str
    summary: str
    status: str # NEW: 用来控制流程
    market_data: dict # 新增 /第7步：升级 State（非常关键）
