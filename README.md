# Migration Rehearsal

Preview database schema migrations and reverse-order rollback SQL without connecting to a database.

## Run

```bash
python migration_rehearsal.py examples/migration.json
python -m unittest discover -s tests -v
```

Supports add_column, rename_column and drop_column operations. JSON input contains an `operations` array. The tool validates identifiers and restricts column types to TEXT, INTEGER, BOOLEAN, REAL and DATE. Destructive operations produce warnings. Dropped data cannot be restored automatically; SQL compatibility varies by database.
