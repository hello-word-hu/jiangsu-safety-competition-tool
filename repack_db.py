"""Rebuild the exe with a new bundled database.db (e.g. built from ~/tiku_learned.csv).

    python repack_db.py <source-exe> <new-database.db> <output.exe>
    python repack_db.py --from-csv learned.csv new.db        # build the sqlite file first

Only the `database.db` entry of the PyInstaller archive is replaced; everything else
is copied from the source exe byte for byte.
"""
import os
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pyi_toc import parse  # noqa: E402
from rebuild import build  # noqa: E402


def db_from_csv(csv_path, db_path):
    rows = {}
    with open(csv_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip().rstrip(",")
            if not line or "," not in line:
                continue
            qid, answers = line.split(",", 1)
            qid, answers = qid.strip(), answers.strip().rstrip(",")
            if qid and answers and qid.lower() != "question":
                rows[qid] = answers          # 同一题号重复采集时，以最后一次为准
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE IF NOT EXISTS "tiku" ("question" TEXT, "answer" TEXT)')
    conn.execute("DELETE FROM tiku")
    conn.executemany("INSERT INTO tiku (question, answer) VALUES (?, ?)", list(rows.items()))
    conn.commit()
    conn.close()
    print("built %s with %d unique questions" % (db_path, len(rows)))
    return db_path


def repack(src_exe, new_db, out_exe):
    blob = open(src_exe, "rb").read()
    meta = parse(blob)
    entry = next(e for e in meta["entries"] if e["name"] == "database.db")
    payload = open(new_db, "rb").read()
    open(out_exe, "wb").write(build(blob, meta, override={entry["idx"]: payload}))
    print("wrote %s (%d bytes) with database.db = %s (%d bytes, %d questions)"
          % (out_exe, os.path.getsize(out_exe), new_db, len(payload),
             sqlite3.connect(new_db).execute("select count(*) from tiku").fetchone()[0]))
    return 0


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--from-csv":
        # --from-csv <csv> <db> [<source-exe> <output-exe>]
        db = db_from_csv(sys.argv[2], sys.argv[3])
        return repack(sys.argv[4], db, sys.argv[5]) if len(sys.argv) >= 6 else 0
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    return repack(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    sys.exit(main())
