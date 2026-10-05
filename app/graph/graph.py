from langgraph.graph import StateGraph,START,END
from app.state import StockState

from app.agents.news_agent import news_agent
# from app.agents.planner import planner

# from app.agents.ask_user import ask_user
from app.agents.risk_agent import risk_agent
from app.agents.summary_agent import summary_agent

# Step 12.1 import
from app.agents.technical import technical_agent
from app.agents.market import market_agent

print('1-StateGraph')
# 这里不是创建 Graph。 而是在创建： Graph Builder（建造器）,Step 12.2 创建 Graph
builder = StateGraph(StockState)
# Expected type 'Type[StateT ≤: TypedDictLikeV1 | TypedDictLikeV2 | DataclassLike | BaseModel]', got 'StockState' instead
print('2-add_node')
# 8-添加节点,Step 12.3 注册节点
# builder.add_node("planner", planner)
# builder.add_node("ask_user", ask_user)

builder.add_node("market", market_agent)
builder.add_node("technical", technical_agent)
builder.add_node("risk", risk_agent)
builder.add_node("summary", summary_agent)
builder.add_node("news", news_agent)

# 最关键 —— 条件函数 # 我们写一个“路由器函数”
# 这个函数的本质：# 它不是业务逻辑，而是：# Graph 调度器（Router）
print('3-route_after_planner')


def route_after_planner(state: StockState):
    status = state.get("status")

    print(f"route_after_planner 判断依据: {state}")
    print(f"route_after_planner 返回: {status}")

    if status == "OK":
        return "market"

    return "ask_user"


# [3]- 第8步：添加 Conditional Edge,这一行是 LangGraph 的灵魂
# planner 输出 state
#          │
#          ▼
# route_after_planner(state)
#          │
#          ▼
# 决定下一节点
# builder.add_conditional_edges(
#     "planner", route_after_planner
# )

# [3]* 第9步：连接普通边
# 9-告诉 Graph 从哪里开始
# builder.add_edge(START, "planner")
# Step 12.4 设计 Multi-Agent 流程
# 并行执行（核心）
builder.add_edge(START, "market")
builder.add_edge(START, "technical")
builder.add_edge(START, "news")

# 第10步：Market → Technical → Summary,继续补链路：
# 注意：planner 的出口只由上面的条件边决定。
# 不要再加 builder.add_edge("planner", END)，
# 那会让 planner 有两条出边，条件路由被架空。

# 然后汇聚
builder.add_edge("market", "risk")
builder.add_edge("technical", 'risk')
builder.add_edge("news", 'risk')
builder.add_edge("risk", 'summary')
builder.add_edge("summary", END)

# 第11步：编译,这里才真正生成： Graph Runtime。
graph = builder.compile()
