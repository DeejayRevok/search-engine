from os.path import join, dirname


API_VERSION = "v1"
ALEMBIC_INI_PATH = join(
    dirname(
        dirname(
            __file__,
        )
    ),
    "alembic.ini",
)
