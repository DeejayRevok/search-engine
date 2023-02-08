from infrastructure.aiohttp.middlewares import load as load_middlewares


def load() -> None:
    load_middlewares()
