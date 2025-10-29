-- Complex SELECT with multiple clauses
SELECT id, name, email, age
FROM users
WHERE active = TRUE AND age > 18
ORDER BY name ASC
LIMIT 10 OFFSET 5;
