/Users/andy_mac/PycharmProjects/stock-agent/.venv/bin/python /Users/andy_mac/PycharmProjects/stock-agent/app/main.py 
[bootstrap] 已安装东财封控补丁
1-StateGraph
2-add_node
3-route_after_planner
Planner Start Working...
Planner 分析问题：分析信维通信
planner返回 state : {'stock': '信维通信', 'status': 'OK'}
route_after_planner 判断依据: {'question': '分析信维通信', 'stock': '信维通信', 'status': 'OK'}
route_after_planner 返回: OK
获取市场数据 for: 信维通信
返回 state : {'question': '分析信维通信', 'stock': '信维通信', 'status': 'OK'}
market_node 返回state: {'question': '分析信维通信', 'stock': '信维通信', 'status': 'OK'}
 技术分析：信维通信
{'question': '分析信维通信', 'stock': '信维通信', 'market_data': {'found': True, 'name': '信维通信', 'code': '300136', 'price': 51.23, 'change': -1.42, 'change_pct': -2.7, 'volume': 256458.0, 'amount': 1328931969.3, 'open': 53.06, 'high': 53.29, 'low': 51.01, 'prev_close': 52.65, 'volume_unit': '手'}, 'technical': {'ma5': np.float64(89.5998447514465), 'ma20': np.float64(92.21236933606336), 'rsi': 25.051294482940037, 'trend': '下跌/震荡', 'signal': '中性'}, 'status': 'DONE_TECH'}


写作日期：
2026-10-05
