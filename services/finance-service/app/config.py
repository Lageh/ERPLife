import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://erplife:erplife@localhost:5432/erplife"
)