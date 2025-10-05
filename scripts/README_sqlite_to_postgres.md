# sqlite_to_postgres_dump

This small utility converts a SQLite database file (`db.sqlite3`) into a Postgres-compatible SQL dump (`dump_postgres.sql`).

Usage:

```powershell
python .\scripts\sqlite_to_postgres_dump.py --sqlite db.sqlite3 --out dump_postgres.sql
```

Notes and caveats:
- The script performs a pragmatic mapping of common types. Complex custom types may need manual fixes.
- Foreign-key constraints, triggers, and views are not fully preserved; you may need to adjust schema manually after importing into Postgres.
- For large databases or robust migrations, consider using `pgloader` or a direct ETL approach.
- The script will attempt to create sequences for tables tracked in `sqlite_sequence` and set them to appropriate values.

After generating `dump_postgres.sql`, create a Postgres database and import the dump:

```powershell
# create database
psql -U <user> -h <host> -p <port> -c "CREATE DATABASE mydb;"
# import
psql -U <user> -h <host> -p <port> -d mydb -f dump_postgres.sql
```

If you want, I can run the script now and show the first lines of the generated SQL file. Provide permission to run it.