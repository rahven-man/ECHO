# ECHO Data Notes (cleaning rules for Phase 1)

## business (150,346 rows)
- attributes: nested dict, values are mostly strings; 13,744 null. Decide: selected columns vs key-value table
- categories: comma-separated, 103 null, whitespace duplicates (strip), split into bridge table
- hours: nested dict, 23,223 null
- review_count min is 5 (dataset limitation, no new businesses)

## review (6,990,280 rows)
- useful/funny/cool have -1 values: clean
- date is string: convert to DATETIME
- text up to 5000 chars: TEXT type

## user (1,987,897 rows)
- friends: drop
- elite: check format after peek (TODO)

## checkin (131,930 rows)
- one row per business, date = comma-separated timestamps: explode into fact rows

## tip (908,915 rows)
- no primary key, text up to 500 chars
- (TODO: add findings after peek)