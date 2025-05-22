# #Copyright (C) 2025 β ORI Inc.
# #Written by Awase Khirni Syed 2025
import sqlparse
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
            if len(parts) < 2:
                continue
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

def convert_file(input_file):
    with open(input_file, 'r') as f:
        sql_script = f.read()

    dbml_result = sql_to_dbml(sql_script)

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_dbml.dbml"

    with open(output_file, 'w') as f:
        f.write(dbml_result)

    print(f"DBML written to: {output_file}")

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sql_to_dbml.py <input_sql_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_file(input_file)
