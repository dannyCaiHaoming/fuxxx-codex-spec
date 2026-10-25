import csv
from pathlib import Path


def export_csv(path, rows):
    """将字符串二维列表覆盖写入调用者指定的 UTF-8 CSV 文件。"""
    with Path(path).open("w", encoding="utf-8", newline="") as output:
        csv.writer(output).writerows(rows)
