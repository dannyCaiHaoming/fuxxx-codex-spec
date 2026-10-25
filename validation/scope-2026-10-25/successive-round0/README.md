# CSV 导出

已完成 [本轮交付](approved-scope.md)：`export_csv(path, rows)` 使用标准库保存 UTF-8 CSV，支持中文、逗号、引号、单元格换行、空列表与覆盖写入；允许调用者指定有效绝对路径。

验证：`python3 -B -m unittest -v`。结果与范围见 [CSV MVP](fucxxx-codex-spec/designs/export.md)。
