USE echo_staging;

-- 1. row count check (expected 908915)
SELECT COUNT(*) FROM tip;

-- 2. Range of text length and compliment_count range (profile: 500 aur 0..6)
SELECT MAX(CHAR_LENGTH(text)), MIN(compliment_count), MAX(compliment_count) FROM tip;

-- 3. duplicate check: whether (user_id, business_id, date) is unique?
SELECT user_id, business_id, date, COUNT(*) AS n
FROM tip
GROUP BY user_id, business_id, date
HAVING COUNT(*) > 1
LIMIT 10;

-- 4. orphan check: tips for which business is not in business table (expected 0)
SELECT COUNT(*)
FROM tip t
LEFT JOIN business b ON b.business_id = t.business_id
WHERE b.business_id IS NULL;