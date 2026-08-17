from app.graph.graph import graph

# 第12步：运行
result = graph.invoke(
    {
        "question": "分析信维通信"
    }
)
print(result)
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
# planner(state)
#     │
#     ▼
# state["stock"] = "信维通信"
#     │
#     ▼
# END
#     │
#     ▼
# Output = {
#     "question": "分析信维通信",
#     "stock": "信维通信"
# }