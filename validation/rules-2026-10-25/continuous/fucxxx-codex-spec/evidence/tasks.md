# MVP 验收记录
环境：本项目 continuous 目录，Python 3.13.10，标准库、离线，无 Git 仓库。
基线：app.py 两接口抛 NotImplementedError；原 2 项测试运行均报该错误。
最终命令：`python3 -B -m unittest -v`，退出码 0，Ran 4 tests，OK。
- test_roundtrip：缺失文件为空、添加两项、标题 trim、中文读回、id 不同。
- test_blank：空标题抛 ValueError，不创建文件。
- test_blank_preserves_existing_file：已存在内容逐字节保持不变。
- test_reopen_in_new_process：实际新 Python 进程添加第二项并读回，跨进程 id 不同，原进程再读结果一致；文件内容是 UTF-8 中文。
复核：主会话自检实际代码；校验先于读写，只捕获不存在文件错误，其他异常不静默忽略。不属于独立评审。
最终代码定位：
- app.py: `638f0dbd6a1d5780c926e8678810d43207089db991f48efad11056c870234b77`
- test_app.py: `bbc065e7fa7d72c34d63c605303af3c960cdf6b388cb16b5fb25c066b56a8faf`
计划原判据已保存在上面的测试对应说明；实现、测试和复核均结束，活动计划可移除。
未验证：并发写入、磁盘故障、损坏数据恢复，不作这些能力承诺。当前 README MVP 无未完成项。
