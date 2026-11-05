"""Plan reversible SQL schema migration operations without executing SQL."""
import argparse
import json
import re
import sys

IDENT=re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def identifier(value):
    if not isinstance(value,str) or not IDENT.fullmatch(value):
        raise ValueError("invalid SQL identifier: "+str(value))
    return '"'+value+'"'

def plan(operations):
    if not isinstance(operations,list): raise ValueError("operations must be an array")
    forward=[]
    rollback=[]
    warnings=[]
    for i,op in enumerate(operations):
        if not isinstance(op,dict): raise ValueError("operation must be an object")
        action=op.get("action")
        table=identifier(op.get("table"))
        if action=="add_column":
            column=identifier(op.get("column"))
            typ=op.get("type")
            if typ not in ("TEXT","INTEGER","BOOLEAN","REAL","DATE"):
                raise ValueError("unsupported column type")
            forward.append(f"ALTER TABLE {table} ADD COLUMN {column} {typ};")
            rollback.append(f"ALTER TABLE {table} DROP COLUMN {column};")
        elif action=="rename_column":
            old=identifier(op.get("from"))
            new=identifier(op.get("to"))
            forward.append(f"ALTER TABLE {table} RENAME COLUMN {old} TO {new};")
            rollback.append(f"ALTER TABLE {table} RENAME COLUMN {new} TO {old};")
        elif action=="drop_column":
            column=identifier(op.get("column"))
            forward.append(f"ALTER TABLE {table} DROP COLUMN {column};")
            rollback.append("-- MANUAL RESTORE REQUIRED: "+table+"."+column)
            warnings.append("step "+str(i+1)+": dropping a column destroys data")
        else: raise ValueError("unsupported action")
    return {"forward":forward,"rollback":list(reversed(rollback)),"warnings":warnings}

def main(argv=None):
    p=argparse.ArgumentParser(description="Preview SQL migration and rollback steps")
    p.add_argument("file")
    args=p.parse_args(argv)
    try:
        with open(args.file,encoding="utf-8") as f: data=json.load(f)
        if not isinstance(data,dict): raise ValueError("input must be an object")
        result=plan(data.get("operations"))
    except (OSError,ValueError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
