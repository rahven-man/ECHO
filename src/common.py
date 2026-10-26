"""Shared helpers for ECHO ETL scripts: DB engine, logging, JSONL reader."""

"This is a shared helper module, the function defined here are used in multiple ETL scripts. It is not intended to be run directly."
import json
import logging
import os
from itertools import islice
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
LOG_DIR = ROOT / "logs"

load_dotenv(ROOT / ".env")


def get_engine():
    """Build a SQLAlchemy engine from .env values (utf8mb4)."""
    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        query={"charset": "utf8mb4"},
    )
    return create_engine(url)


def get_logger(name):
    """Logger that writes to console and logs/<name>.log."""
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:          # avoid duplicate handlers on re-import
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for handler in (logging.StreamHandler(),
                    logging.FileHandler(LOG_DIR / f"{name}.log", encoding="utf-8")):
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


def read_jsonl(path, limit=None):
    """Generator: yield one parsed JSON object per line, never the whole file."""
    with open(path, "r", encoding="utf-8") as f:
        for line in islice(f, limit):   # limit=None means read everything
            yield json.loads(line)


def batched(iterable, size):
    """Generator: yield lists of up to `size` items."""
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk