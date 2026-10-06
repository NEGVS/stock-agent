# ============ 1. 创建字典 ============
# 方式一：花括号
person = {"name": "Alice", "age": 25, "city": "Shanghai"}

# 方式二：dict() 构造函数
person2 = dict(name="Bob", age=30)

# 方式三：从键值对列表
person3 = dict([("name", "Charlie"), ("age", 35)])

print("创建:", person)

# ============ 2. 读取值 ============
print("name:", person["name"])  # 键不存在会 KeyError
print("age:", person.get("age"))  # 安全读取，不存在返回 None
print("job:", person.get("job", "N/A"))  # 可指定默认值

# ============ 3. 判断键是否存在 ============
print("name 存在:", "name" in person)  # True
print("job  存在:", "job" in person)  # False

# ============ 4. 修改 / 新增 ============
person["age"] = 26  # 修改已有键
person["job"] = "Engineer"  # 新增键值对
print("修改后:", person)

# ============ 5. 删除 ============
del person["city"]  # 删除指定键
job = person.pop("job", "N/A")  # 弹出并返回值
print("pop 的 job:", job)
print("删除后:", person)

# ============ 6. 遍历 ============
# 遍历键
for key in person:
    print(f"  key: {key}")

# 遍历键值对
for key, value in person.items():
    print(f"  {key} = {value}")

# 只遍历值
for value in person.values():
    print(f"  value: {value}")

# ============ 7. 常用方法 ============
print("所有键:", list(person.keys()))
print("所有值:", list(person.values()))
print("键值对:", list(person.items()))
print("长度:", len(person))

# ============ 8. 合并字典 ============
defaults = {"role": "user", "level": 1}
merged = {**defaults, **person}  # Python 3.5+
# 或 Python 3.9+ 用 | 运算符
# merged = defaults | person
print("合并:", merged)

# ============ 9. 嵌套字典 ============
data = {
    "stock": "600519",
    "market_data": {"price": 1800.0, "volume": 10000},
    "tags": ["白酒", "龙头"],
}
print("股价:", data["market_data"]["price"])

# ============ 10. 字典推导式 ============
squares = {x: x ** 2 for x in range(1, 6)}
print("推导式:", squares)
