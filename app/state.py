from typing import TypedDict


# 整个 Graph 的共享内存。
# Dictionary 比对象快。
# TypedDict 又有类型提示。

class StockState(TypedDict):
    # 这就是所有节点共享的数据。
    question: str
    stock: str
    news: str
    technical: str
    fund: str
    risk: str
    summary: str
