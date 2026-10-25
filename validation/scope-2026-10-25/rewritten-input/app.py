from pathlib import Path
def export_csv(path, rows):
    Path(path).write_text("\n".join(",".join(row) for row in rows), encoding="utf-8")
