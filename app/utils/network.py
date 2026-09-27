"""网络会话配置。

akshare 底层用 requests，而 requests 会自动读取 macOS 的系统代理
（scutil --proxy 里那个 HTTPProxy）。
代理软件没开时，请求会被塞给一个没人监听的端口，直接 ProxyError。

这里显式控制代理，优先级：
    环境变量 HTTP_PROXY / HTTPS_PROXY  >  .env 里的 STOCK_PROXY  >  直连

也就是说：不配置就是直连，不会被系统代理悄悄劫持。
"""
import os

from dotenv import load_dotenv

load_dotenv()

_PROXY_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")


def get_proxy() -> str | None:
    """返回当前生效的代理地址，没有则返回 None（直连）。"""
    for key in _PROXY_KEYS:
        value = os.getenv(key)
        if value:
            return value

    return os.getenv("STOCK_PROXY") or None


def setup_proxy() -> str | None:
    """把代理设置同步到环境变量，让 requests / urllib3 都能读到。

    必须在 import akshare 之前调用，否则底层连接池已经按旧配置建好了。
    """
    proxy = get_proxy()

    for key in ("HTTP_PROXY", "HTTPS_PROXY"):
        if proxy:
            os.environ[key] = proxy
        else:
            os.environ.pop(key, None)

    # 让本地回环地址绕过代理，避免代理软件把自己转进去
    os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

    return proxy
