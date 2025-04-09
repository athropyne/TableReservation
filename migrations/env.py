from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.schemas import metadata
from src.core.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

__user = settings.POSTGRES_USER
__password = settings.POSTGRES_PASSWORD
__socket = settings.DB_SOCKET
__dbname = settings.POSTGRES_DB
config.set_main_option('sqlalchemy.url', f"postgresql+psycopg://{__user}:{__password}@{__socket}/{__dbname}")
target_metadata = metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
