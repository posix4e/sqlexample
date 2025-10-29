# Automated SQL Parser from BNF Specification

This is a complete example of generating a SQL parser implementation from a formal BNF (Backus-Naur Form) specification in a standardized, automated manner.

## Overview

The system consists of three main components:

1. **sql.bnf** - The formal SQL language specification in BNF notation
2. **sql_generator.py** - Reads and analyzes the BNF grammar structure
3. **sql_parser.py** - Complete SQL parser implementation based on the BNF spec

## How It Works

### Step 1: Define SQL Language in BNF

The `sql.bnf` file contains a formal specification of SQL:

```bnf
<select_stmt> ::= "SELECT" <select_list>
                  "FROM" <table_references>
                  <where_clause>?
                  <group_by_clause>?
                  <order_by_clause>?

<expression>  ::= <or_expr>
<or_expr>     ::= <and_expr> ("OR" <and_expr>)*
<and_expr>    ::= <not_expr> ("AND" <not_expr>)*
```

### Step 2: Parse BNF Specification

The `BNFParser` class in `sql_generator.py` reads the BNF file and creates an internal representation (Grammar object) with production rules.

### Step 3: Parser Implementation

The `sql_parser.py` implements a complete parser following the BNF structure:
- **Lexer**: Tokenizes SQL input with ~80 token types
- **Parser**: Recursive descent parser following the BNF structure
- **AST Nodes**: 30+ data structures representing SQL constructs
- **No Execution**: Only parses SQL, does not execute it

### Step 4: Use SQL Parser

The parser validates SQL syntax and builds an Abstract Syntax Tree (AST).

## Usage

```bash
# Analyze the BNF grammar structure
python3 sql_generator.py

# Run the SQL parser with examples
python3 sql_parser.py

# Run the comprehensive test suite
python3 test_sql_parser.py
```

## Testing

The project includes a comprehensive test suite with 80+ tests covering:

- **Valid SQL**: Tests for all supported SQL statements (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP)
- **Invalid SQL**: Tests that malformed SQL properly raises syntax errors
- **Unicode Support**: Tests for international characters (Chinese, Arabic, Japanese, emoji, etc.)
- **Edge Cases**: Whitespace handling, very long strings, deeply nested expressions

### Test Categories

1. **TestValidSQL** - Valid SQL statements that should parse successfully
2. **TestInvalidSQL** - Invalid SQL that should raise syntax errors
3. **TestUnicodeSupport** - International character and emoji support
4. **TestEdgeCases** - Boundary conditions and special cases

## Example SQL Statements

The parser can handle:

```sql
SELECT * FROM users;
SELECT id, name FROM users WHERE age > 18;
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
UPDATE users SET email = 'new@example.com' WHERE id = 1;
DELETE FROM users WHERE age < 18;
CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));
SELECT COUNT(*) FROM orders WHERE status = 'completed';
```

## Key Features

- **Standardized Format**: Uses industry-standard BNF notation for SQL grammar
- **Parse-Only**: Validates SQL syntax without execution (perfect for tools, linters, formatters)
- **Complete Coverage**: Handles DDL (CREATE, DROP, ALTER) and DML (SELECT, INSERT, UPDATE, DELETE)
- **Extensible**: Easy to modify the BNF to add new SQL features or dialects
- **Rich AST**: 30+ AST node types representing all SQL constructs

## Architecture

```
sql.bnf (SQL Specification)
    ↓
BNFParser (Grammar analyzer)
    ↓
Grammar (Internal representation)
    ↓
sql_parser.py (Hand-crafted implementation following BNF)
    ├── Lexer (Tokenization with 80+ token types)
    ├── Parser (Recursive descent following BNF rules)
    └── AST (Abstract syntax tree)
```

## Supported SQL Features

### DML Statements
- **SELECT**: `*`, column lists, aliases, JOINs, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT/OFFSET
- **INSERT**: Single/multiple rows, INSERT INTO ... SELECT
- **UPDATE**: SET clause with WHERE conditions
- **DELETE**: With WHERE clause

### DDL Statements
- **CREATE TABLE**: Column definitions, data types, constraints (PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT, etc.)
- **DROP TABLE**: With IF EXISTS
- **ALTER TABLE**: ADD COLUMN (simplified)

### Expressions
- Arithmetic operators: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`
- Logical operators: `AND`, `OR`, `NOT`
- Special operators: `BETWEEN`, `IN`, `LIKE`, `IS NULL`
- Functions: `COUNT(*)`, `SUM()`, etc.
- Subqueries in expressions and FROM clause

## Adding SQL Features

To extend the parser with new SQL features:

1. Modify `sql.bnf` to include new grammar rules
2. Update `sql_parser.py` to implement the new rules
3. Add corresponding AST node types if needed

For example, to add UNION:

```bnf
<select_stmt> ::= <select_query> ("UNION" ("ALL")? <select_query>)*
```

## Continuous Integration

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/sql-parser-ci.yml`) that:

- **Analyzes** the BNF grammar structure
- **Tests** the parser across Python 3.9-3.12 on Linux, macOS, and Windows
- **Validates** Unicode support across different locales
- **Stress tests** with large queries (1000+ columns, 500+ INSERT rows)
- **Runs continuously** on schedule and on-demand
- **Checks** code quality and syntax

### CI Jobs

1. `analyze-grammar` - Validates and analyzes the BNF grammar
2. `test-parser` - Runs tests across multiple Python versions and OSes
3. `test-unicode` - Specifically tests Unicode/international character support
4. `stress-test` - Performance testing with large queries
5. `integration-test` - Full end-to-end pipeline test
6. `continuous-testing` - Runs tests in a loop for consistency checking
7. `code-quality` - Syntax and style checks

## Unicode Support

The parser fully supports Unicode/UTF-8:
- ✓ International characters in string literals (Chinese, Arabic, Japanese, etc.)
- ✓ Emoji in data values
- ✓ Mixed scripts in the same string
- ✓ Right-to-left text (Arabic, Hebrew)
- ✓ Combining diacritical marks
- ✓ All Unicode code points in strings

## References

- [Backus-Naur Form (BNF)](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)
- [Recursive Descent Parsing](https://en.wikipedia.org/wiki/Recursive_descent_parser)
- [Compiler Design Principles](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
