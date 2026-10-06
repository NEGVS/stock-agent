# ============ 1. 整数 int ============
a = 42
b = -7
c = 0xFF          # 十六进制
d = 0b1010        # 二进制
print(f"int:        {a}, {b}, {c}, {d}")

# ============ 2. 浮点数 float ============
x = 3.14
y = 2.5e3         # 科学计数法
print(f"float:      {x}, {y}")

# ============ 3. 复数 complex ============
z = 3 + 4j
print(f"complex:    {z}  (real={z.real}, imag={z.imag})")

# ============ 4. 布尔 bool ============
flag = True
print(f"bool:       {flag}")

# ============ 5. 字符串 str ============
s = "Hello, Python"
print(f"str:        {s}")

# ============ 6. 列表 list（有序、可变）============
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(f"list:       {fruits}")

# ============ 7. 元组 tuple（有序、不可变）============
point = (10, 20)
print(f"tuple:      {point}")

# ============ 8. 范围 range ============
r = range(5)
print(f"range:      {list(r)}")

# ============ 9. 字典 dict（键值对）============
person = {"name": "Alice", "age": 25}
print(f"dict:       {person}")

# ============ 10. 集合 set（无序、不重复）============
s = {1, 2, 3, 3}
print(f"set:        {s}")

# ============ 11. 冻结集合 frozenset（不可变集合）============
fs = frozenset([1, 2, 3])
print(f"frozenset:  {fs}")

# ============ 12. 字节 bytes（不可变）============
b = b"hello"
print(f"bytes:      {b}")

# ============ 13. 字节数组 bytearray（可变）============
ba = bytearray(b"hello")
print(f"bytearray:  {ba}")

# ============ 14. 内存视图 memoryview ============
mv = memoryview(b"ABCD")
print(f"memoryview: {mv}")

# ============ 15. 空值 NoneType ============
n = None
print(f"NoneType:   {n}")