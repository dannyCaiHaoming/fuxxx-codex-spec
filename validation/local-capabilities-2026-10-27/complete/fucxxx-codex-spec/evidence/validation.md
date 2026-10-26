# 标题规范化验证

日期：2026-10-27 Asia/Tokyo。环境：Python 3.13.10，本隔离 complete 目录，无 Git 仓库。
原始 app.py：def normalize_title(title): return title；原始测试仅普通 title 返回不变。
先保存总设计、MVP、实施 plan 与交接，再补测试；原实现执行 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v，退出 1，4 个测试方法中 10 个子用例失败，覆盖首尾空白未处理和空标题未拒绝，普通标题通过。
修复后同一命令退出 0，4 个测试方法全部通过（普通标题 1，首尾空白 3，内部空白 3，空标题拒绝 4，合计 11 个输入）。错误类型及消息精确断言。
实际差量：app.py 添加注解、strip、空结果 ValueError；test_app.py 保留原用例并补以上契约用例。requirements.md 和 AGENTS.md 未修改。
自检实现直接作用于原始缺口，内部空白没有重新分词；本函数即产品入口，实际调用已通过，无 mock。未进行独立评审；非字符串输入不属于约定契约，无服务、UI、持久化或模型能力声明。
计划判据及结果已转入此证据和设计，临时 plan 将删除，不保留唯一事实在临时文档。

## 最终文件版本
- app.py: SHA256 ceb07ff43d297a7170e360910df81c288d5c78bb2a1083964b347f3dc9df5af6
- test_app.py: SHA256 e42a9faa3759dd666272c4441fcf990583626fc5f4282ff6029c8764a3ed1c59
- requirements.md: SHA256 bc4534418b437c7c73fac15c18ae3066a432eccbcab5f398d06bd8288a581c9a
- AGENTS.md: SHA256 503b5bd26a7f47435f543a244a276bbdbfa007759ae327bbec01d85519e6ca8b
