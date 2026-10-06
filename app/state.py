from typing import TypedDict, Dict, Any, Optional, List, Annotated
import operator


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
    stock: Optional[str]  # 未识别到股票时为 None

    # 各节点的产出

    news: Dict[str, Any]

    fund: str

    risk: Dict[str, Any]

    summary: Dict[str, Any]

    market_data: Dict[str, Any]  # 新增 /第7步：升级 State（非常关键）

    technical: Dict[str, Any]  # 👈 新增：技术分析结果

    # 流程控制
    status: str  # NEW: 用来控制流程

    messages: List[str] # Agent之间沟通日志
    # 你现在 messages: List[str] 没有加 reducer。如果多个节点都返回 messages，默认会覆盖，而不是追加。
    # messages: Annotated[List[str], operator.add]  # Agent之间沟通日志


    memory: Dict[str, Any]   # 👈 新增,升级 State（加入历史记忆）
#      # 这就是所有节点共享的数据。
#     question: str
#     stock: Optional[str]
#     news: str
#     technical: str
#     fund: str
#     risk: str
#     summary: str
#     status: str # NEW: 用来控制流程
#     market_data: dict # 新增 /第7步：升级 State（非常关键）
