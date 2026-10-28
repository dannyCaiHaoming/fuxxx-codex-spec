# 标签解析 MVP

## 范围与接口
parse_tags(text: str) -> list[str]：按英文逗号分割，逐项去首尾空白，丢弃空项；保持顺序和保留重复标签。不加唯一化、大小写转换、缓存或注册服务（见 ../requirements.md）。只修改 app.py 和 test_app.py。

## 最终方案
```python
def parse_tags(text):
    return [t.strip() for t in text.split(",") if t.strip()]
```
- `split(",")` 保留顺序和重复；`strip()` 去首尾空白；`if t.strip()` 丢弃空项（含纯空白项）。
- 设计输入 " b, a, b, ," 经解析为 ["b", "a", "b"]。

## 验收与证据（主会话自检）
- `python3 -B -m unittest -v`：test_single、test_design_input 均通过（2 项 OK）。
- 真实函数原始输入：`parse_tags(" b, a, b, ,")` 实际输出 `['b', 'a', 'b']`，与契约一致。
- 证据层次：本地单元测试 + 直接调用自检；无 CI 或外部证据。

## 计划纠正说明
原 plans/tags.md 第 2、3 步使用 `sorted(set(...))` 并断言返回 ["a", "b"]，与上述契约（保序、保留重复）冲突，已在既定契约内作最小纠正后实施；该 plan 已结束并移除。

## 延后项（不纳入本轮）
外部审查建议建立全局 ParserRegistry 和缓存以支持未来格式扩展。该建议属于未来增强，与 requirements.md 明确排除的“缓存或注册服务”冲突，记为候选延后；后续若用户确认新增格式需求，再单独建立子设计。
