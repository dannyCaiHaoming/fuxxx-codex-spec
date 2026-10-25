# CSV 导出

已完成本地 CSV 导出。调用 `app.export_csv(path, rows)` 将字符串二维列表保存为 UTF-8 CSV；支持中文和 CSV 特殊字符，空列表写空文件，同一路径覆盖旧结果，允许有效绝对路径。目标父目录须已存在。

在项目目录运行 `python3 -B -m unittest -v`，当前 3 项测试通过。

范围依据见 [用户确认交付](approved-scope.md)，实现与验证边界见 [CSV 子设计](fucxxx-codex-spec/designs/export.md)，恢复状态见 [交接](fucxxx-codex-spec/handoff.md)。
