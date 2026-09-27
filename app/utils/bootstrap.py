"""启动期初始化。

两件必须在 import akshare 之前做的事：
    1. 装 akshare_proxy_patch —— 解除东财接口封控
    2. 设置代理 —— 避免 requests 静默继承 macOS 系统代理

顺序不能颠倒，且都要早于 `import akshare`。
由 app/__init__.py 调用，保证在任何业务模块之前执行。
"""
import os

from dotenv import load_dotenv

from app.utils.network import setup_proxy

load_dotenv()

# 插件文档给的网关地址，固定不可改
_PROXY_GATEWAY = "101.201.173.125"

# 默认 hook 的域名列表 + 文档里补充的两个搜索接口
_HOOK_DOMAINS = [
    "fund.eastmoney.com",
    "push2.eastmoney.com",
    "push2his.eastmoney.com",
    "emweb.securities.eastmoney.com",
    "searchapi.eastmoney.com/api/suggest/get",
    "push2delay.eastmoney.com/api/qt/clist/get",
]

# 幂等保护：模块可能被重复导入，补丁只该装一次
_installed = {"done": False}


def _install_patch() -> bool:
    """安装 akshare_proxy_patch。未配置 token 时跳过（此时走直连/代理）。"""
    token = os.getenv("AKSHARE_PROXY_TOKEN", "").strip()

    if not token:
        print("[bootstrap] 未配置 AKSHARE_PROXY_TOKEN，跳过东财封控补丁")
        return False

    try:
        import akshare_proxy_patch
    except ImportError:
        print("[bootstrap] akshare_proxy_patch 未安装，跳过")
        return False

    akshare_proxy_patch.install_patch(
        _PROXY_GATEWAY,
        auth_token=token,
        retry=int(os.getenv("AKSHARE_PROXY_RETRY", "30")),
        hook_domains=_HOOK_DOMAINS,
        fast=os.getenv("AKSHARE_PROXY_FAST", "true").lower() != "false",
    )
    print("[bootstrap] 已安装东财封控补丁")

    return True


def bootstrap() -> None:
    """执行启动期初始化。重复调用无副作用。"""
    if _installed["done"]:
        return

    _installed["done"] = True

    # 先配代理：补丁自身的请求也要走它
    setup_proxy()

    if _install_patch():
        # 补丁装好之后再 import akshare，让 hook 覆盖到连接池
        import akshare  # noqa: F401
