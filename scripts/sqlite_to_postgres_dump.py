"""
Generate a Postgres-compatible SQL dump from an existing SQLite3 database file.

Usage:
  python scripts/sqlite_to_postgres_dump.py --sqlite db.sqlite3 --out dump_postgres.sql

This script attempts to:
 - Read SQLite schema (tables, columns, types, primary keys, not nulls, defaults)
 - Convert common SQLite types to Postgres types
 - Emit CREATE TABLE statements for Postgres
 - Emit INSERT statements for data with proper escaping
 - Emit sequences for AUTOINCREMENT integer PKs and set them to max values

It's a pragmatic tool for small-to-medium sqlite DBs. For complex schemas and large data sets, consider using pgloader or a direct ETL to Postgres.

"""
import argparse
import sqlite3
import re
import sys
from datetime import datetime

TYPE_MAP = [
    (re.compile(r"INT", re.I), "INTEGER"),
    (re.compile(r"CHAR|CLOB|TEXT", re.I), "TEXT"),
    (re.compile(r"BLOB", re.I), "BYTEA"),
    (re.compile(r"REAL|FLOA|DOUB", re.I), "DOUBLE PRECISION"),
    (re.compile(r"NUMERIC|DECIMAL", re.I), "NUMERIC"),
    (re.compile(r"BOOLEAN", re.I), "BOOLEAN"),
    (re.compile(r"DATE", re.I), "DATE"),
    (re.compile(r"TIME", re.I), "TIMESTAMP"),
]

def map_type(sqlite_type):
    if not sqlite_type:
        return "TEXT"
    for pattern, pg_type in TYPE_MAP:
        if pattern.search(sqlite_type):
            return pg_type
    return "TEXT"

def quote_ident(name):
    return '"{}"'.format(name.replace('"','""'))

def quote_literal(val):
    if val is None:
        return 'NULL'
    if isinstance(val, bytes):
        return "E'\\x' || decode('" + val.hex() + "','hex')"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val)
    s = s.replace("\\","\\\\")
    s = s.replace("'","''")
    return "'{}'".format(s)


def get_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    return cur.fetchall()


def get_columns(conn, table):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({quote_ident(table)})")
    # cid, name, type, notnull, dflt_value, pk
    cols = cur.fetchall()
    return cols


def get_foreign_keys(conn, table):
    cur = conn.cursor()
    try:
        cur.execute(f"PRAGMA foreign_key_list({quote_ident(table)})")
    except sqlite3.OperationalError:
        return []
    # id, seq, table, from, to, on_update, on_delete, match
    rows = cur.fetchall()
    fks = []
    for r in rows:
        # sqlite returns tuples where 'table' is at index 2 and 'from' is at 3 and 'to' at 4
        fks.append({'table': r[2], 'from': r[3], 'to': r[4], 'on_update': r[5], 'on_delete': r[6]})
    return fks


def get_indexes(conn, table):
    cur = conn.cursor()
    cur.execute(f"PRAGMA index_list({quote_ident(table)})")
    indexes = cur.fetchall()
    result = []
    for idx in indexes:
        # seq, name, unique, origin, partial
        name = idx[1]
        cur.execute(f"PRAGMA index_info({quote_ident(name)})")
        cols = [r[2] for r in cur.fetchall()]
        cur.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND name=?", (name,))
        sql = cur.fetchone()
        sql = sql[0] if sql and sql[0] else None
        result.append((name, idx[2], cols, sql))
    return result


def dump(sqlite_path, out_path):
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    tables = get_tables(conn)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('-- Dumped by sqlite_to_postgres_dump.py on {}\n\n'.format(datetime.utcnow().isoformat()))
        f.write('BEGIN;\n\n')

        sequences = []
        fk_constraints = []
        boolean_alterations = []

        for name, sql in tables:
            f.write('-- Table: {}\n'.format(name))
            cols = get_columns(conn, name)
            # Build CREATE TABLE
            col_defs = []
            pks = []
            for c in cols:
                cid, colname, coltype, notnull, dflt_value, pk = c
                pgtype = map_type(coltype)
                coldef = f"{quote_ident(colname)} {pgtype}"
                if notnull:
                    coldef += ' NOT NULL'
                if dflt_value is not None:
                    # sqlite default values sometimes include parentheses or quotes; leave as is for simplicity
                    coldef += ' DEFAULT ' + dflt_value
                col_defs.append(coldef)
                if pk:
                    pks.append(colname)
            pk_clause = ''
            if pks:
                pk_clause = ', PRIMARY KEY (' + ', '.join(quote_ident(x) for x in pks) + ')'
            f.write(f'CREATE TABLE {quote_ident(name)} (\n')
            f.write('  ' + ',\n  '.join(col_defs) + pk_clause + '\n');
            f.write(');\n\n')

            # Data
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {quote_ident(name)}")
            rows = cur.fetchmany(1000)
            cols_names = [c[1] for c in cols]
            # Prepare boolean detection: track allowed boolean-like values per column
            bool_candidates = {c[1]: True for c in cols}
            while rows:
                for r in rows:
                    values = [quote_literal(r[col]) for col in cols_names]
                    # boolean detection: narrow candidates
                    for col in cols_names:
                        if not bool_candidates.get(col):
                            continue
                        v = r[col]
                        if v is None:
                            continue
                        sv = str(v).lower()
                        if sv in ('0', '1', 'true', 'false', 't', 'f') or sv.isdigit() and sv in ('0','1'):
                            continue
                        # not a boolean-like value
                        bool_candidates[col] = False
                    f.write('INSERT INTO {} ({}) VALUES ({});\n'.format(quote_ident(name), ', '.join(quote_ident(c) for c in cols_names), ', '.join(values)))
                rows = cur.fetchmany(1000)
            f.write('\n')
            # After scanning table rows, record boolean-like columns (require at least one non-null value)
            for col, is_bool in bool_candidates.items():
                if not is_bool:
                    continue
                # check if column has any non-null values at all
                cur.execute(f"SELECT 1 FROM {quote_ident(name)} WHERE {quote_ident(col)} IS NOT NULL LIMIT 1")
                if cur.fetchone():
                    boolean_alterations.append((name, col))

            # Indexes
            idxs = get_indexes(conn, name)
            for idx in idxs:
                idx_name, unique, idx_cols, idx_sql = idx
                if idx_sql:
                    # Convert sqlite index SQL to Postgres - simplistic
                    f.write(idx_sql.replace('AUTOINCREMENT',''))
                    f.write('\n')
                else:
                    uq = 'UNIQUE ' if unique else ''
                    f.write(f'CREATE {uq}INDEX {quote_ident(idx_name)} ON {quote_ident(name)} ({", ".join(quote_ident(c) for c in idx_cols)});\n')
            f.write('\n')

            # If table has an autoincrement-like integer primary key, create sequence and set it
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
            if cur.fetchone():
                cur.execute("SELECT seq FROM sqlite_sequence WHERE name=?", (name,))
                seqrow = cur.fetchone()
                if seqrow:
                    seqval = seqrow[0]
                    seqname = f"{name}_id_seq"
                    sequences.append((seqname, name, seqval))

            # Collect foreign keys
            fks = get_foreign_keys(conn, name)
            for fk in fks:
                # we'll add constraints after all tables are created
                fk_constraints.append((name, fk))

        # Emit sequences
        for seqname, table, val in sequences:
            f.write(f"CREATE SEQUENCE {quote_ident(seqname)};\n")
            f.write(f"SELECT setval('{seqname}', {val}, true);\n\n")

        # Emit foreign key constraints (as ALTER TABLE ... ADD CONSTRAINT)
        for table, fk in fk_constraints:
            cons_name = f"{table}_{fk['from']}_fkey"
            on_update = '' if not fk.get('on_update') else f" ON UPDATE {fk['on_update']}"
            on_delete = '' if not fk.get('on_delete') else f" ON DELETE {fk['on_delete']}"
            f.write(f"ALTER TABLE {quote_ident(table)} ADD CONSTRAINT {quote_ident(cons_name)} FOREIGN KEY ({quote_ident(fk['from'])}) REFERENCES {quote_ident(fk['table'])} ({quote_ident(fk['to'])}){on_update}{on_delete};\n")
        f.write('\n')

        # Emit boolean alterations
        for table, col in boolean_alterations:
            # Convert 0/1 text/int to true/false and then alter column type
            f.write(f"-- Convert column {quote_ident(col)} on {quote_ident(table)} to boolean\n")
            f.write(f"UPDATE {quote_ident(table)} SET {quote_ident(col)} = CASE WHEN {quote_ident(col)} IN ('1', 1, 'true', 't', 'True') THEN 't' ELSE 'f' END;\n")
            f.write(f"ALTER TABLE {quote_ident(table)} ALTER COLUMN {quote_ident(col)} TYPE boolean USING ({quote_ident(col)}::boolean);\n\n")

        f.write('COMMIT;\n')

    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sqlite', default='db.sqlite3', help='Path to sqlite file')
    parser.add_argument('--out', default='dump_postgres.sql', help='Output SQL file')
    args = parser.parse_args()
    dump(args.sqlite, args.out)
    print(f'Wrote {args.out}')

if __name__ == '__main__':
    main()
