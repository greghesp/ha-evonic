"""Evonic Error Exceptions"""


class EvonicError(Exception):
    """Generic Evonic Exception"""


class EvonicUnsupportedFeature(Exception):
    """Unsupported feature exception"""


class EvonicConnectionError(EvonicError):
    """Evonic connection exception"""


class EvonicConnectionTimeoutError(EvonicConnectionError):
    """Evonic connection Timeout exception"""


class EvonicConnectionClosed(EvonicConnectionError):
    """Evonic Websocket connection has been closed"""