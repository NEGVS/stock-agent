from app.utils.bootstrap import bootstrap

# 必须在任何业务模块导入之前执行。
#
# akshare 在 import 时就会建立连接池，akshare_proxy_patch 的 hook
# 也必须在那一刻之前装好，否则补丁对已经创建的连接不生效。
# Python 保证包被导入时先执行 __init__.py，所以放在这里是最早的时机。
bootstrap()
