from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import DATABASE_URL
from app.db import Base
from app import models  # noqa: F401


# Alembic Config object (lê alembic.ini e permite acessar configs)
config = context.config

# Configura logging com base no alembic.ini (opcional, mas padrão)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata das tabelas (vem dos seus models via Base)
target_metadata = Base.metadata


def get_url() -> str:
    """
    Retorna a URL do banco.
    Usamos DATABASE_URL para manter o padrão: configuração via env var + default local.
    """
    return DATABASE_URL


def run_migrations_offline() -> None:
    """
    Modo offline:
    - não abre conexão real com o banco
    - gera SQL "como texto"
    Útil em alguns pipelines, mas em dev normalmente usamos o modo online.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_schemas=True,
        version_table="alembic_version",
        version_table_schema="finance",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Modo online:
    - abre conexão real com o banco
    - aplica migrações de verdade
    É o modo padrão para dev local.
    """
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
            version_table="alembic_version",
            version_table_schema="finance",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()