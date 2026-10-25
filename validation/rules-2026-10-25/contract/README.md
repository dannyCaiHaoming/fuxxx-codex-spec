# 标题规范
Python 标准库，运行 `python3 -B -m unittest -v`。
接口 `normalize_title(title)`：先去首尾空白，空标题或超过 40 个 Python 字符抛 `ValueError`，合法标题完整返回，不静默截断。
当前 v2 已通过本地单元验收；范围仅为任务标题校验。
恢复与契约详见[当前交接](fucxxx-codex-spec/handoff.md)和[标题设计](fucxxx-codex-spec/designs/title.md)。
