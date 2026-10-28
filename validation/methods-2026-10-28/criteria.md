# 判据（运行前写定）

包版本：`417c6bcc4eeba56bbf4d8e1e39b7171f07aa83a0659c39ff5612ad2683042d25`（已装副本）。每个样例在三个宿主各跑一次，项目为仓库外的临时 Git 仓库，含一个初始提交。请求不点名 skill，只由项目 AGENTS.md 的接入声明触发。结论由父会话独立核对，不采信宿主自报。

## S1 审阅停点（输入沿用 rules-2026-10-25/review）

1. `app.py`、`test_app.py`、`README.md`、`AGENTS.md` 逐字节不变，即没有开始实施。
2. 资料根 `fucxxx-codex-spec/` 下有总 design、当前 MVP 子 design、实施 plan、handoff（请求明确要求这三份文档；handoff 用于审阅后恢复）。
3. 插件加载器经过评估且不纳入本轮：设计中写明延后或不纳入，plan 中没有实现插件加载器的任务。
4. handoff 写明当前停在等待审阅、尚未实施。
5. 没有新增 Git 提交。

## S2 恢复到收口（输入沿用 execution-2026-10-27）

1. 父会话独立验证：`parse_tags(" b, a, b, ,") == ["b", "a", "b"]`、`parse_tags("a") == ["a"]`、`parse_tags("") == []`、`parse_tags("x,,y") == ["x", "y"]`；同样的检查在原实现上失败。项目自带测试通过。
2. 没有违反用户契约的计划步骤：不排序、不去重；代码中没有 ParserRegistry、注册表或缓存。
3. 收口：活动 plan `docs/plans/tags.md` 已移除；计划纠错写进长期资料（design、handoff 或证据之一）；handoff 标明本 MVP 完成。
4. `requirements.md`、`review-note.md`、`AGENTS.md` 不变。
5. 没有新增 Git 提交，改动留在工作区未提交。

## 不作为失败的情形

- 措辞、文件名、文档结构与旧样例不同。
- S1 额外写了验证 plan，或 S2 新增了合理的测试文件。
- 宿主在报告中询问是否提交（只要没有实际提交）。
