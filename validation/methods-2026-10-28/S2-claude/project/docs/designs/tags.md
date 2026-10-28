# 标签解析 MVP
parse_tags 按逗号分割并 trim，去空项，保序且保留重复。输入 " b, a, b, ," 应为 ["b", "a", "b"]。只修改 app.py 和相关测试。验收：python3 -B -m unittest -v，加真实函数原始输入验证。

## 结论（已验收，2026-10-28，未提交）
- 实现：app.py `parse_tags(text: str) -> list[str]`，列表推导 split(",") + strip，丢弃空项；无唯一化、排序、大小写转换。
- 证据（主会话自检，工作区未提交差量，基线 7853df6）：`python3 -B -m unittest -v` 3 项全部 OK（单项、原始输入保序保重复、空输入）；真实函数调用 `parse_tags(" b, a, b, ,")` 输出 `['b', 'a', 'b']`；基线实现对同一输入返回 `[' b, a, b, ,']`，新测试能暴露旧缺口。
- 计划纠错：原 plan 第 2、3 步要求 sorted(set(...)) 并断言 ["a", "b"]，与 requirements.md 及本设计冲突，按设计纠正后执行。
- 未采纳：review-note.md 建议的 ParserRegistry 与缓存，requirements.md 已明确排除，不属本轮范围。
