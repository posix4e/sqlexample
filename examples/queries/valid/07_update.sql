-- UPDATE statement
UPDATE users
SET active = FALSE, last_login = NULL
WHERE age < 18;
