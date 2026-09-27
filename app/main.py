from app.graph.graph import graph

# 第12步：运行
result = graph.invoke(
    {
        "question": "分析信维通信"
    }
)
print(result)

# 当前实际链路（与 app/graph/graph.py 保持一致）
#
# User Input
#     │
#     ▼
# State = {
#     "question": "分析信维通信"
# }
#     │
#     ▼
# START
#     │
#     ▼
# planner                     app/agents/planner.py
#     │  extract_stock(question) → "信维通信"
#     │  status = "OK"
#     ▼
# route_after_planner         graph.py  条件路由
#     │
#     ├── status == "OK"      → market
#     └── status == 其他      → ask_user
#     │
#     ▼
# market                      app/agents/market.py
#     │  get_stock_info(stock)
#     │  market_data = {...}     取数失败时 found=False，不中断流程
#     ▼
# technical                   app/agents/technical.py
#     │  technical = "..."
#     ▼
# END
#
# 未识别到股票时的分支：
# route_after_planner → ask_user → END
#
# 注意：planner 的出口只由条件边决定（graph.py 的 add_conditional_edges）。
# 不要再加 builder.add_edge("planner", END)，那会让 planner 有两条出边，
# 条件路由被架空，market / technical 永远不会执行。
