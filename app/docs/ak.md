我已经
安装了
add akshare-proxy-patch==0.5.0
token：
202609270KOOVB2A

针对 akshare、efinance、yfinance、aktools、daily_stock_analysis 的🐒插件补丁，解决 stock_zh_a_spot_em、stock_zh_a_hist、get_realtime_quotes 等东财接口报错问题和 Yahoo YFRateLimitError 问题。并对 akshare 部分接口进行多线程加速处理。

✨ 特性
解决 akshare 或 aktools 的 stock_zh_a_spot_em、stock_zh_a_hist 接口报错问题
解决 efinance 的 get_realtime_quotes 等接口报错问题
解决 yfinance Yahoo接口国内无法使用问题
解决 daily_stock_analysis 的数据获取报错问题
多线程加速 stock_zh_a_spot_em、stock_individual_fund_flow_rank 等 akshare 接口

安装并升级官方 akshare 或 efinance 包

安装 akshare-proxy-patch 插件

pip install akshare-proxy-patch==0.5.0

# python 文件顶部添加如下代码
# 重要：插件引入和调用一定要放到最顶部！不能在 akshare 或 efinance 之后引入！

import akshare_proxy_patch

akshare_proxy_patch.install_patch(
    "101.201.173.125",
    auth_token="你的TOKEN",
    retry=30,
    # 封控的域名列表，可自行调整
    hook_domains=[
      "fund.eastmoney.com",
      "push2.eastmoney.com",
      "push2his.eastmoney.com",
      "emweb.securities.eastmoney.com",
      "searchapi.eastmoney.com/api/suggest/get",
      "push2delay.eastmoney.com/api/qt/clist/get"
    ],
    fast=True
)

# --------------------------
# 后续你的业务代码保持不变
# --------------------------

# 假如你使用 akshare
import akshare as ak
df = ak.stock_zh_a_spot_em()

# 假如你使用 efinance
import efinance as ef
ef.stock.get_realtime_quotes()


install_patch 参数说明
ip
网关，不可修改
auth_token
TOKEN 授权凭证
retry
重试次数，默认为30，建议保持不变
hook_domains
封控的域名列表，插件会 hook 住这些域名的请求，解除封控。插件已默认涵盖了一些常见函数的域名。
可点击 akshare 或 efinance 函数查看接口源码对应的 URL，根据封控情况细化可以降低积分消耗。
如只用到 stock_zh_a_spot_em 这个接口，hook_domains 可设置为 ["https://82.push2.eastmoney.com/api/qt/clist/get"]。
fast
是否启用 akshare 多线程加速，默认开启，加速函数列表如下
所有用到 fetch_paginated_data 分页函数的接口，如 stock_zh_a_spot_em、stock_sh_a_spot_em、stock_board_industry_cons_em 等
stock_individual_fund_flow_rank
stock_sector_fund_flow_rank
fund_money_fund_info_em
fund_graded_fund_info_em
fund_etf_fund_info_em
fund_fh_em
fund_cf_em
fund_fh_rank_em
如有其他函数加速需求欢迎反馈

