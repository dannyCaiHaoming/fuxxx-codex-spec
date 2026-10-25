# 标题工具设计

本轮目标是 README 的两个独立函数可用，并由两个独立内部子 Agent 分别实现，共享当前项目目录，由主会话复核收口。

- `normalize_title(title)`：字符串 strip 后非空则返回；空字符串或纯空白抛出 ValueError。
- `render_title(title)`：使用标准库 HTML 转义，覆盖 &、<、>、双引号和单引号，返回 str。不会隐式调用 normalize，也不删除空白。
- 非字符串输入不新增契约。不引入插件、HTTP、配置系统或第三方依赖。
- 离线，只改本项目；不安装、commit、push。此目录不是 Git 仓库，使用文件 SHA256 记录基线。

## 当前状态与导航

方案已明确；实现尚未开始。初始两个测试均因 NotImplementedError 报错，不能宣称功能可用。

当前实施依据：[活动计划](plans/title-tools.md)；恢复入口：[handoff](handoff.md)。主会话持有设计、计划、handoff 和共享测试文件唯一写入权。

验收：子 Agent 定向检查后，主会话审阅全部实际差量，运行 `python3 -B -m unittest -v`，补验空字符串、Unicode 空白、普通文本、全部转义字符、空标题渲染和返回类型。通过后回写结果，保存判据和证据，再删除已结束计划。
