import re

from sqlalchemy import create_engine, inspect, text

from .config import settings
from .database import Base, engine
from . import models  # noqa: F401

# SQLAlchemy no permite parametrizar identificadores (nombres de base de datos) en DDL;
# en su lugar se valida contra una lista blanca estricta antes de interpolar el nombre.
VALID_DB_NAME = re.compile(r"^[A-Za-z0-9_]+$")


def ensure_database() -> None:
    if not VALID_DB_NAME.match(settings.db_name):
        raise ValueError(
            "db_name invalido: solo se permiten letras, numeros y guion bajo."
        )

    server_engine = create_engine(settings.database_server_url, pool_pre_ping=True, future=True)
    # settings.db_name ya fue validado arriba contra VALID_DB_NAME (solo [A-Za-z0-9_]):
    # no es un CREATE DATABASE con datos de usuario, y los identificadores no se pueden
    # bindear como parametros en DDL, asi que la interpolacion aqui es segura.
    create_db_sql = text(  # nosemgrep: avoid-sqlalchemy-text
        f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    with server_engine.connect() as connection:
        connection.execute(create_db_sql)
        connection.commit()
    server_engine.dispose()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def ensure_schema_updates() -> None:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if "users" not in table_names:
        return

    user_columns = {column["name"] for column in inspector.get_columns("users")}
    with engine.connect() as connection:
        if "is_admin" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_admin TINYINT(1) NOT NULL DEFAULT 0"))
        connection.commit()


def init_database() -> None:
    ensure_database()
    create_tables()
    ensure_schema_updates()


if __name__ == "__main__":
    init_database()
    print(f"Database ready: {settings.db_name}")
