可以这样写一个测试脚本：

```python
import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)

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
```

### 几个注意点

- **`decode_responses=True`** 建议加上，否则 `get` 返回的是 `b'world'` 这种 bytes。
- 测试连通性用 **`r.ping()`**，成功会返回 `True`。
- 如果 Redis 设置了密码，需要加：

```python
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    password="你的密码",
    decode_responses=True,
)
```

- 如果本地还没装 Redis 服务，需要先启动 Redis，否则会报 `ConnectionError`。

运行后如果输出 `ping: True`，说明 Redis 连接正常。

---
需要我把这个测试脚本保存成 `test_redis.py` 吗？
