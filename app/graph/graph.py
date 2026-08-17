from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from app.agents.planner import planner

from app.agents.ask_user import ask_user
from app.agents.technical import technical

from app.agents.market import market_node
from app.state import StockState

print('1-StateGraph')
# 这里不是创建 Graph。 而是在创建： Graph Builder（建造器）
builder = StateGraph(StockState)

print('2-add_node')
# 8-添加节点
builder.add_node("planner", planner)
builder.add_node("ask_user", ask_user)
builder.add_node("market", market_node)
builder.add_node("technical", technical)

# 最关键 —— 条件函数 # 我们写一个“路由器函数”
# 这个函数的本质：# 它不是业务逻辑，而是：# Graph 调度器（Router）
print('3-route_after_planner')


def route_after_planner(state: StockState):
    # if state["status"] == "OK":
    #     return "technical"
    if state["status"] == "NEED_INPUT":
        print(f"route_after_planner 返回state: {state}")

        return "ask_user"
    # 让 Planner 决定是否进入 Market：
    if state["status"] == "OK":
        print(f"route_after_planner 返回state: {state}")
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
builder.add_conditional_edges(
    "planner", route_after_planner
)

# [3]* 第9步：连接普通边
# 9-告诉 Graph 从哪里开始
builder.add_edge(START, "planner")
# 10-告诉 Graph 哪里结束
builder.add_edge("planner", END)
# 第10步：Market → Technical → Summary,继续补链路：
builder.add_edge("market", "technical")
builder.add_edge("technical", END)
builder.add_edge("ask_user", END)

# 第11步：编译,这里才真正生成： Graph Runtime。
graph = builder.compile()
