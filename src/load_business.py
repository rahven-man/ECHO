"""Load business JSONL into echo_staging.business (truncate-and-reload)."""
import argparse
import json

from common import RAW_DIR, batched, get_engine, get_logger, read_jsonl

SOURCE = RAW_DIR / "yelp_academic_dataset_business.json"
BATCH_SIZE = 5000

INSERT_SQL = """
INSERT INTO business
(business_id, name, address, city, state, postal_code, latitude, longitude,
 stars, review_count, is_open, attributes, categories, hours)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

log = get_logger("load_business")


def to_json(value):
    """dict -> JSON string; None stays None (becomes SQL NULL)."""
    return None if value is None else json.dumps(value)


def to_row(rec):
    return (
        rec["business_id"], rec["name"], rec["address"], rec["city"],
        rec["state"], rec["postal_code"], rec["latitude"], rec["longitude"],
        rec["stars"], rec["review_count"], rec["is_open"],
        to_json(rec["attributes"]), rec["categories"], to_json(rec["hours"]),
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
        cur.execute("TRUNCATE TABLE business")     # makes the run rerunnable

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
    