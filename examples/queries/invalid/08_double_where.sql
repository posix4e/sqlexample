-- Invalid: Multiple WHERE clauses
SELECT * FROM users WHERE id = 1 WHERE name = 'Alice';
