# Stock Agent

AI-powered stock analysis system using LangGraph and multi-agent architecture.

## Features

- Multi-Agent collaboration architecture
- LangGraph state graph orchestration
- Real-time stock data analysis
- Intelligent investment recommendations

## Setup

```bash
# Install dependencies
uv sync

# Set environment variables
cp .env.example .env
# Edit .env and add your DASHSCOPE_API_KEY
```

## Usage

```bash
python main.py
```

对应的文档
【LangGraph】
https://my.feishu.cn/docx/B8uQdQ16wo5eAax0v6cciK60nad




stock-agent/

├── pyproject.toml
├── uv.lock
│
├── app
│   ├── graph
│   │   └── workflow.py
│   │
│   ├── agents
│   │   ├── planner_agent.py
│   │   ├── news_agent.py
│   │   ├── financial_agent.py
│   │   ├── risk_agent.py
│   │   └── report_agent.py
│   │
│   ├── tools
│   │   ├── stock_tool.py
│   │   └── news_tool.py
│   │
│   ├── api
│   │   └── app.py
│   │
│   └── models
│       └── state.py
│
└── tests
