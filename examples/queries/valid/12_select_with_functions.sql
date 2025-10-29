-- SELECT with aggregate functions
SELECT COUNT(*), AVG(age), MAX(created_at)
FROM users
WHERE active = TRUE
GROUP BY country
HAVING COUNT(*) > 10;
