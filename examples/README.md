# SQL Parser Examples

This directory contains example SQL queries for testing the SQL parser.

## Directory Structure

```
examples/
├── queries/
│   ├── valid/      # SQL queries that should parse successfully
│   └── invalid/    # SQL queries that should fail to parse
```

## Valid Queries

The `valid/` directory contains 12 example SQL queries covering:
- Simple SELECT statements
- SELECT with WHERE, JOIN, ORDER BY, LIMIT, OFFSET
- INSERT statements (single and multiple rows)
- UPDATE statements
- DELETE statements
- CREATE TABLE statements (with various constraints)
- DROP TABLE statements
- Aggregate functions with GROUP BY and HAVING

## Invalid Queries

The `invalid/` directory contains 10 example SQL queries that should fail parsing:
- Missing required clauses (FROM, SET, VALUES)
- Incorrect keyword order
- Incomplete expressions
- Syntax errors
- Invalid table definitions

## Running Tests

To test all queries:

```bash
python3 test_queries.py
```

This will:
1. Generate the SQL parser
2. Test all valid queries (should parse successfully)
3. Test all invalid queries (should fail to parse)
4. Report results

## CI/CD

The GitHub Actions workflow `.github/workflows/test-parser.yml` automatically runs these tests on:
- Every push to main/master
- Every pull request
- Multiple Python versions (3.8 - 3.12)
