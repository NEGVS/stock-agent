# 架构级升级 Multi-Agent[多智能体协作系统]

Planner → Market → Technical → END

```
单链 Graph
        ↓
Multi-Agent Graph
```

```
                ┌──────────────┐
                │  Planner     │
                └──────┬───────┘
                       │
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
Market Agent     Technical Agent     News Agent
     │                 │                 │
     └────────────┬────┴────┬──────────┘
                  ▼         ▼
             Risk Agent   Summary Agent
                  │         │
                  └────┬────┘
                       ▼
                    END
```

第5步：设计 Multi-Agent 的关键原则
记住一句话：
 不要让 Agent 互相调用
 让 Agent 只读 State + 写 State