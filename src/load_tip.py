"""Load tip JSONL into echo_staging.tip (truncate-and-reload)."""
import argparse

from common import RAW_DIR, batched, get_engine, get_logger, read_jsonl

SOURCE = RAW_DIR / "yelp_academic_dataset_tip.json"
BATCH_SIZE = 5000

INSERT_SQL = """
INSERT INTO tip
(business_id, user_id, text, date, compliment_count)
VALUES (%s, %s, %s, %s, %s)
"""

log = get_logger("load_tip")


def to_row(rec):
    return (
        rec["business_id"], rec["user_id"], rec["text"], rec["date"],
        rec["compliment_count"],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="load only the first N rows (for testing)")
    args = parser.parse_args()

    log.info("Start. source=%s limit=%s", SOURCE.name, args.limit)
    conn = get_engine().raw_connection()
    try:
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE tip")     # makes the run rerunnable

        total = 0
        rows = (to_row(r) for r in read_jsonl(SOURCE, args.limit))
        for chunk in batched(rows, BATCH_SIZE):
            cur.executemany(INSERT_SQL, chunk)
            conn.commit()
            total += len(chunk)
            log.info("Inserted %s rows so far", f"{total:,}")

        log.info("Done. Total rows loaded: %s", f"{total:,}")
    except Exception:
        conn.rollback()
        log.exception("Load failed")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()