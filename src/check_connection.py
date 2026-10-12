import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

url = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    query={"charset": "utf8mb4"},
)
engine = create_engine(url)

with engine.connect() as conn:
    print("Connected to:", conn.execute(text("SELECT DATABASE()")).scalar())
    print("MySQL version:", conn.execute(text("SELECT VERSION()")).scalar())
    print("Charset:", conn.execute(text("SELECT @@character_set_database")).scalar())