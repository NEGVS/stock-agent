import re

from app.state import StockState

# Planner 不是“分析器”，而是：
# 决策 + 信息抽取器
# 它做的事情：
# 从 question → 提取 stock
# 并决定下一步状态

# 常见问法里，股票名前后会带这些词，解析时先剥掉
_NOISE_PATTERN = re.compile(
    r"(请|帮我|帮忙|麻烦|我想|我要|看一下|看看|分析下|分析一下|分析|评估|研究|怎么样|如何|怎样|的|股票|个股)"
)

# A 股股票名的形态：3~8 个汉字。
# 这条规则用来挡掉“你好”“今天天气”这类根本不是股票名的回答——
# 先剥噪声再返回，会把整句话剩下的部分当股票名，必须有形态兜底。
_STOCK_NAME_PATTERN = re.compile(r"^[一-龥A-Za-z]{3,8}$")


def extract_stock(question: str) -> str | None:
    """从自然语言问题里抽出股票名。

    目前是"先剥噪声、再校验形态"的朴素做法。
    后续接 LLM 做实体识别时，只需要替换这个函数。
    """
    if not question:
        return None

    candidate = _NOISE_PATTERN.sub("", question).strip(" 　，,。.?？!！")

    if not _STOCK_NAME_PATTERN.match(candidate):
        return None

    return candidate


# 写第一个node
def planner(state: StockState):
    print('Planner Start Working...')
    question = state["question"]
    print(f"Planner 分析问题：{question}")

    stock = extract_stock(question)

    if stock:
        result = {"stock": stock, "status": "OK"}
    else:
        result = {"stock": None, "status": "NEED_INPUT"}

    print(f"planner返回 state : {result}")

    return result


# node的本质
# 输入 State
# ↓
# 处理
# ↓
# 返回 State（只需返回自己改动的字段，其余由图合并）
