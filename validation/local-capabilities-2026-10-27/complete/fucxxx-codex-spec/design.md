# 标题规范化：总设计

来源：../requirements.md；设计已定，已实现，真实函数验收通过。
本地单用户 Python 标准库函数工具。调用者传入字符串，app.normalize_title 去除首尾空白后返回标题；内部空白原样保留，空结果抛 ValueError("empty title")。
仅一个 MVP：[标题规范化](designs/title.md)。不增加服务、登录、分类、持久化或非字符串输入契约。
职责链：调用者 → normalize_title → 字符串或 ValueError。根因是当前函数直接返回输入；在该函数内使用 str.strip() 和空结果判定即可补齐全部已定行为，无需新抽象。
验收入口为现有 unittest，覆盖普通标题、首尾空白、内部空白、空字符串及纯空白。
导航：[当前交接](handoff.md)。当前仅局部设计和计划，不修改 AGENTS.md 或正式接入。

## 交付结论
本次契约全部实现，自检及现有 unittest 入口验收通过，详见[验证证据](evidence/validation.md)。无阻塞或未完成需求；未正式接入、安装、提交、推送或发布。活动 plan 在结论保存后移除。
