-- SELECT without FROM clause
-- FROM is optional in SQL grammar to support queries like:
--   SELECT 1 + 1;
--   SELECT CURRENT_TIMESTAMP;
--   SELECT 'Hello, World!';
-- While "SELECT * WHERE id = 1" is syntactically valid,
-- it's semantically meaningless (WHERE without FROM).
-- Semantic validation should be handled in a separate analysis phase.
SELECT * WHERE id = 1;
