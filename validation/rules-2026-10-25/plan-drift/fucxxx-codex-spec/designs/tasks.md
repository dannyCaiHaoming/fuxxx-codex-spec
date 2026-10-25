# 当前任务 MVP
状态：已实现并在本地通过验收，未提交。

已定：本地 JSON 持久化，add_task(path, title) 返回含 id、title 的 dict；list_tasks(path) 每次重新从磁盘读取列表，文件不存在时返回空列表。
标题去首尾空白，空白抛 ValueError 并在读取／写入前拒绝；UTF-8 直接保存中文。UUID 与文件中现有 id 比对，保证顺序调用时同文件 id 唯一。
不做：插件加载器、通知、HTTP、配置引擎。当前标准库足够。

## 计划纠偏与实现结论
原计划要求插件前置、只验收文件存在且延后空标题校验，与 README 和本设计冲突。删除插件前置，恢复完整验收；没有改变已定契约。app.py 直接以标准库 JSON、pathlib、uuid 实现，无需存储抽象。

## 验证证据
2026-10-25，当前本地 app.py 与 test_app.py，Python 标准库环境。
基线 python3 -B -m unittest -v：原有 2 项测试均因 NotImplementedError 失败。
实现后同一命令：4 项测试全部通过。
- test_roundtrip：不存在文件返回空列表、中文标题去空白、两个 id 不同、列表完整读回。
- test_blank：空标题抛 ValueError，未创建文件。
- test_blank_preserves_existing_file：已有文件拒绝空白标题，字节内容不变。
- test_reopen_in_new_process：中文 UTF-8 落盘，独立 Python 进程经 list_tasks 读回相同任务。

复核方式为主会话直接检查实现与契约并运行上述测试，未进行独立评审。验证了真实本地文件持久化和新进程读回；没有 Web UI 或外部服务验收。当前单调用者顺序读写，未承诺并发写入或崩溃恢复；这些不属于本轮验收。当前范围无遗留阻塞。
已结束实施 plan 的判据与结果保存在此，活动 plan 已移除。
[总设计](../design.md)
