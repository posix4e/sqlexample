#!/usr/bin/env python3
"""
SQL Parser Generator

This script generates a SQL parser from the sql.bnf grammar file.
The generated parser file (sql_parser.py) is read-only and should not be checked into the repo.
"""

import os
import sys
from pathlib import Path


def convert_bnf_to_lark(bnf_content):
    """
    Convert BNF grammar to Lark EBNF format.

    Lark uses a slightly different syntax:
    - Uses : instead of ::=
    - Uses lowercase for rules
    - Uses UPPERCASE for terminals
    - Supports regex patterns directly
    """

    lark_grammar = """
// SQL Grammar for Lark Parser
// Auto-generated from sql.bnf - DO NOT EDIT

start: statement_list

statement_list: statement (";" statement)* ";"?

statement: select_stmt
         | insert_stmt
         | update_stmt
         | delete_stmt
         | create_table_stmt
         | drop_table_stmt
         | alter_table_stmt

// SELECT Statement
select_stmt: SELECT select_list FROM table_references where_clause? group_by_clause? having_clause? order_by_clause? limit_clause?

select_list: "*"
           | select_item ("," select_item)*

select_item: expression (AS identifier)?

table_references: table_reference ("," table_reference)*

table_reference: table_name alias_clause?
               | join_clause

alias_clause: AS? identifier

join_clause: table_reference join_type JOIN table_reference ON expression

join_type: INNER | LEFT | RIGHT | FULL | CROSS |

where_clause: WHERE expression

group_by_clause: GROUP BY expression_list

having_clause: HAVING expression

order_by_clause: ORDER BY order_item ("," order_item)*

order_item: expression (ASC | DESC)?

limit_clause: LIMIT number (OFFSET number)?

// INSERT Statement
insert_stmt: INSERT INTO table_name ("(" column_list ")")? insert_source

insert_source: VALUES value_list ("," value_list)*
             | select_stmt

column_list: identifier ("," identifier)*

value_list: "(" expression_list ")"

// UPDATE Statement
update_stmt: UPDATE table_name SET assignment_list where_clause?

assignment_list: assignment ("," assignment)*

assignment: identifier "=" expression

// DELETE Statement
delete_stmt: DELETE FROM table_name where_clause?

// CREATE TABLE Statement
create_table_stmt: CREATE TABLE (IF NOT EXISTS)? table_name "(" column_def_list ")"

column_def_list: column_def ("," column_def)*

column_def: identifier data_type column_constraint*

data_type: INT | INTEGER | BIGINT | SMALLINT
         | VARCHAR "(" number ")"
         | CHAR "(" number ")"
         | TEXT
         | DECIMAL "(" number ("," number)? ")"
         | FLOAT | DOUBLE | REAL
         | DATE | TIME | TIMESTAMP | DATETIME
         | BOOLEAN | BOOL
         | BLOB

column_constraint: PRIMARY KEY
                 | NOT NULL
                 | NULL
                 | UNIQUE
                 | AUTO_INCREMENT
                 | DEFAULT literal
                 | CHECK "(" expression ")"
                 | REFERENCES table_name "(" identifier ")"

// DROP TABLE Statement
drop_table_stmt: DROP TABLE (IF EXISTS)? table_name

// ALTER TABLE Statement
alter_table_stmt: ALTER TABLE table_name alter_action

alter_action: ADD COLUMN column_def
            | DROP COLUMN identifier
            | MODIFY COLUMN column_def
            | RENAME TO table_name

// Expressions
expression: or_expr

or_expr: and_expr (OR and_expr)*

and_expr: not_expr (AND not_expr)*

not_expr: NOT not_expr
        | comparison_expr

comparison_expr: additive_expr (comparison_op additive_expr)?
               | additive_expr BETWEEN additive_expr AND additive_expr
               | additive_expr IN "(" expression_list ")"
               | additive_expr LIKE additive_expr
               | additive_expr IS NOT? NULL

comparison_op: "=" | "!=" | "<>" | "<" | ">" | "<=" | ">="

additive_expr: multiplicative_expr (("+" | "-") multiplicative_expr)*

multiplicative_expr: unary_expr (("*" | "/" | "%") unary_expr)*

unary_expr: ("+" | "-") unary_expr
          | primary_expr

primary_expr: literal
            | identifier
            | column_ref
            | function_call
            | "(" expression ")"
            | "(" select_stmt ")"

column_ref: identifier "." identifier
          | identifier "." identifier "." identifier

function_call: identifier "(" (expression_list | "*")? ")"

expression_list: expression ("," expression)*

// Basic tokens
table_name: identifier

identifier: CNAME

literal: number
       | string
       | TRUE | FALSE
       | NULL

number: NUMBER

string: SQL_STRING

// Terminals (Keywords - case insensitive)
SELECT: "select"i
FROM: "from"i
WHERE: "where"i
INSERT: "insert"i
INTO: "into"i
VALUES: "values"i
UPDATE: "update"i
SET: "set"i
DELETE: "delete"i
CREATE: "create"i
TABLE: "table"i
DROP: "drop"i
ALTER: "alter"i
ADD: "add"i
COLUMN: "column"i
MODIFY: "modify"i
RENAME: "rename"i
TO: "to"i
IF: "if"i
NOT: "not"i
EXISTS: "exists"i
AS: "as"i
JOIN: "join"i
INNER: "inner"i
LEFT: "left"i
RIGHT: "right"i
FULL: "full"i
CROSS: "cross"i
ON: "on"i
GROUP: "group"i
BY: "by"i
HAVING: "having"i
ORDER: "order"i
ASC: "asc"i
DESC: "desc"i
LIMIT: "limit"i
OFFSET: "offset"i
AND: "and"i
OR: "or"i
BETWEEN: "between"i
IN: "in"i
LIKE: "like"i
IS: "is"i
NULL: "null"i
TRUE: "true"i
FALSE: "false"i
PRIMARY: "primary"i
KEY: "key"i
UNIQUE: "unique"i
DEFAULT: "default"i
CHECK: "check"i
REFERENCES: "references"i
AUTO_INCREMENT: "auto_increment"i

// Data types
INT: "int"i
INTEGER: "integer"i
BIGINT: "bigint"i
SMALLINT: "smallint"i
VARCHAR: "varchar"i
CHAR: "char"i
TEXT: "text"i
DECIMAL: "decimal"i
FLOAT: "float"i
DOUBLE: "double"i
REAL: "real"i
DATE: "date"i
TIME: "time"i
TIMESTAMP: "timestamp"i
DATETIME: "datetime"i
BOOLEAN: "boolean"i
BOOL: "bool"i
BLOB: "blob"i

// Import standard tokens
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS

// Custom tokens
SQL_STRING: /'[^']*'/
COMMENT: /--.*?$/m

// Ignore comments
%ignore COMMENT
"""

    return lark_grammar


def generate_parser_code(grammar):
    """Generate the Python parser code using the grammar."""

    parser_code = '''"""
SQL Parser - Auto-generated from sql.bnf
DO NOT EDIT THIS FILE MANUALLY

This file is generated by generate_parser.py and should not be checked into version control.
It is marked as read-only to prevent accidental modifications.
"""

try:
    from lark import Lark, Tree, Token
except ImportError:
    print("Error: lark-parser is not installed.")
    print("Please install it with: pip install lark-parser")
    import sys
    sys.exit(1)


# Grammar definition
GRAMMAR = """
''' + grammar + '''
"""


class SQLParser:
    """
    SQL Parser class that wraps the Lark parser.

    Usage:
        parser = SQLParser()
        tree = parser.parse("SELECT * FROM users WHERE id = 1")
        print(tree.pretty())
    """

    def __init__(self):
        """Initialize the parser with the SQL grammar."""
        self.parser = Lark(GRAMMAR, start='start', parser='lalr')

    def parse(self, sql_text):
        """
        Parse SQL text and return the parse tree.

        Args:
            sql_text (str): SQL statement or statements to parse

        Returns:
            Tree: Lark parse tree

        Raises:
            Exception: If parsing fails
        """
        return self.parser.parse(sql_text)

    def parse_file(self, filepath):
        """
        Parse SQL from a file.

        Args:
            filepath (str): Path to SQL file

        Returns:
            Tree: Lark parse tree
        """
        with open(filepath, 'r') as f:
            sql_text = f.read()
        return self.parse(sql_text)


def main():
    """Parse SQL from stdin and output the AST."""
    import sys

    parser = SQLParser()

    # Read all input from stdin
    sql_input = sys.stdin.read().strip()

    if not sql_input:
        print("Error: No input provided", file=sys.stderr)
        print("Usage: echo 'SELECT * FROM users;' | python sql_parser.py", file=sys.stderr)
        print("   or: python sql_parser.py < query.sql", file=sys.stderr)
        sys.exit(1)

    try:
        # Parse the input
        tree = parser.parse(sql_input)

        # Output the AST in pretty format for inspection
        print("=" * 80)
        print("SQL Input:")
        print("=" * 80)
        print(sql_input)
        print()
        print("=" * 80)
        print("Parse Tree (AST):")
        print("=" * 80)
        print(tree.pretty())
        print()
        print("=" * 80)
        print("Parse successful ✓")
        print("=" * 80)

    except Exception as e:
        print("=" * 80, file=sys.stderr)
        print("Parse Error:", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

    return parser_code


def make_readonly(filepath):
    """Make the file read-only."""
    os.chmod(filepath, 0o444)


def main():
    """Main function to generate the parser."""
    script_dir = Path(__file__).parent
    bnf_file = script_dir / "sql.bnf"
    output_file = script_dir / "sql_parser.py"

    print("SQL Parser Generator")
    print("=" * 60)

    # Check if BNF file exists
    if not bnf_file.exists():
        print(f"Error: BNF file not found at {bnf_file}")
        sys.exit(1)

    print(f"Reading grammar from: {bnf_file}")

    # Read BNF file
    with open(bnf_file, 'r') as f:
        bnf_content = f.read()

    # Convert to Lark grammar
    print("Converting BNF to Lark EBNF format...")
    lark_grammar = convert_bnf_to_lark(bnf_content)

    # Generate parser code
    print("Generating parser code...")
    parser_code = generate_parser_code(lark_grammar)

    # Remove old file if it exists (it might be read-only)
    if output_file.exists():
        print(f"Removing existing parser file...")
        os.chmod(output_file, 0o644)  # Make writable first
        output_file.unlink()

    # Write output file
    print(f"Writing parser to: {output_file}")
    with open(output_file, 'w') as f:
        f.write(parser_code)

    # Make it read-only
    print("Setting file as read-only...")
    make_readonly(output_file)

    print()
    print("✓ Parser generated successfully!")
    print(f"✓ Output file: {output_file}")
    print(f"✓ File is read-only and excluded from git")
    print()
    print("To use the parser:")
    print("  from sql_parser import SQLParser")
    print("  parser = SQLParser()")
    print("  tree = parser.parse('SELECT * FROM users;')")
    print()
    print("Note: You need to install lark-parser:")
    print("  pip install lark-parser")


if __name__ == "__main__":
    main()
