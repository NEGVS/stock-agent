import redis
import json

# Memory System
# │
# ├── Short-term Memory（本次对话）
# ├── Long-term Memory（历史股票分析）
# └── Strategy Memory（策略经验）
r = redis.Redis(host='localhost', port=6379, db=0)


def test_redis():
    # 1. 测试连接
    try:
        print("ping:", r.ping())
    except redis.ConnectionError as e:
        print("连接失败:", e)
        exit(1)

    # 2. 测试字符串
    r.set("hello", "world")
    print("get hello:", r.get("hello"))

    # 3. 测试 JSON 存储
    data = {"stock": "600519", "price": 1800.0}
    r.set("stock:latest", json.dumps(data))
    loaded = json.loads(r.get("stock:latest"))
    print("loaded:", loaded)

    # 4. 测试过期时间
    r.set("token", "abc123", ex=60)
    print("ttl token:", r.ttl("token"))

    # 5. 测试 Hash
    r.hset("user:1001", mapping={"name": "Alice", "age": 20})
    print("hgetall:", r.hgetall("user:1001"))

    # 6. 清理测试数据
    r.delete("hello", "stock:latest", "token", "user:1001")


# 写入 Memory
def save_memory(stock: str, data: dict):
    # memory:stock:信维通信
    key = f'memory:stock:{stock}'

    r.set(key, json.dumps(data))


# 读取 Memory
def load_memory(stock: str):
    key = f'memory:stock:{stock}'

    data = r.get(key)

    if not data:
        return None
    return json.loads(data)
