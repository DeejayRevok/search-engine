from infrastructure.database.mappers import load as load_mappers
from infrastructure.database.repositories import load as load_repositories


def load() -> None:
    load_mappers()
    load_repositories()
