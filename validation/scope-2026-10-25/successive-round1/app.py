import csv
from pathlib import Path


def export_csv(path, rows):
    """将字符串行写入 UTF-8 CSV，覆盖指定路径的已有内容。"""
    with Path(path).open("w", encoding="utf-8", newline="") as output:
        csv.writer(output).writerows(rows)
