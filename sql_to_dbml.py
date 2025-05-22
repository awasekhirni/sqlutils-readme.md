# #Copyright (C) 2025 β ORI Inc.
# #Written by Awase Khirni Syed 2025
# uv pip install sqlparse    # install python package.
# Sample output in DBML format
#use https://dbdiagram.io/home/ for visualization of ERD 
"""
Table users {
  id INT [pk]
  username VARCHAR(50) [not null]
  email VARCHAR(100)
  created_at DATETIME
}

Table posts {
  id INT [pk]
  user_id INT
  content TEXT
  created_at DATETIME
}
"""



import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Token
from sqlparse.tokens import Keyword, DML
import os 
import sys

def parse_create_table(statement):
    lines = str(statement).splitlines()
    table_name = None
    columns = []
    for line in lines:
        line = line.strip().rstrip(',')

        if line.upper().startswith('CREATE TABLE'):
            table_name = line.split()[2].strip('`[]')
        elif line and not line.startswith(')'):
            parts = line.split()
            col_name = parts[0].strip('`"[]')
            col_type = parts[1].upper()
            nullable = 'not null' not in line.lower()
            pk = 'primary key' in line.lower()
            columns.append((col_name, col_type, nullable, pk))
    
    return table_name, columns

def sql_to_dbml(sql):
    statements = sqlparse.parse(sql)
    dbml_output = []

    for statement in statements:
        if statement.get_type() != 'CREATE':
            continue

        table_name, columns = parse_create_table(statement)
        if not table_name:
            continue

        dbml_output.append(f"Table {table_name} {{")
        for col_name, col_type, nullable, pk in columns:
            null_str = '' if nullable else ' [not null]'
            pk_str = ' [pk]' if pk else ''
            dbml_output.append(f"  {col_name} {col_type}{null_str}{pk_str}")
        dbml_output.append("}\n")
    
    return '\n'.join(dbml_output)

# Example usage:
if __name__ == "__main__":
    sql_script = """
    CREATE TABLE users (
        id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100),
        created_at DATETIME
    );

    CREATE TABLE posts (
        id INT PRIMARY KEY,
        user_id INT,
        content TEXT,
        created_at DATETIME
    );
    """

    dbml_result = sql_to_dbml(sql_script)
    print(dbml_result)
