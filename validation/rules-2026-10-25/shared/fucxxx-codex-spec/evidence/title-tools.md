# 标题工具交付证据

本项目主会话工具未暴露内部派发能力；上层协调者按原计划代为派发两名独立内部子 Agent，共用本项目目录，无另建用户可见聊天或工作树。下列为派单原文，§0 的共同边界是：读取本项目 AGENTS.md、README、design 和活动计划，仅离线标准库操作；不得安装、commit、push、修改外部资料。normalize 仅写 normalize.py，render 仅写 render.py；主会话唯一维护共享测试、设计、计划和 handoff。

## 1. normalize 派单正文（上层协调者已代为实际派发）

按 §0 读取依据，仅在 normalize.py 实现 normalize_title：strip 后非空返回，空值抛 ValueError。保留函数名及独立职责。运行 `python3 -B -m unittest -v test_tools.Tools.test_normalize`，额外检查空字符串和 Unicode 空白。返回实际差量、验证命令和结果、限制及资源状态，不自行收口主区文档。

## 2. render 派单正文（上层协调者已代为实际派发）

按 §0 读取依据，仅在 render.py 实现 render_title：标准库 HTML 转义 & < > 双引号和单引号，返回 str。不要增加 normalize 依赖。运行 `python3 -B -m unittest -v test_tools.Tools.test_render`，额外检查普通文本、完整五种字符、空字符串和返回类型。返回实际差量、验证命令和结果、限制及资源状态，不自行收口主区文档。


## 子 Agent 返回与主会话独立核验

- `/root/rules_shared_normalize` 返回：normalize.py 已实现 strip、空白拒绝；定向 unittest 1 项及空串、Unicode 空白、内部空格检查通过；无在途进程、临时资源。此处是上层转达的执行者报告。
- `/root/rules_shared_render` 返回：render.py 使用 html.escape(..., quote=True)；定向 unittest 1 项及特殊字符、空串、str、空白保留检查通过；无在途进程、临时资源。此处是上层转达的执行者报告。
- 主会话实际读取两个函数，核对 SHA256 与子 Agent 返回一致；README 与原共享测试在主会话补测前均仍匹配计划基线。函数职责独立，标准库实现满足 README，无新增依赖或服务。
- 初始两个函数均 raise NotImplementedError；初始 `python3 -B -m unittest -v` exit 1，两个错误。最终原始失败样例保留。
- 主会话在 test_tools.py 增加两项边界测试：空串、ASCII/Unicode 空白、内部空格保留，以及五种转义字符、空串/普通中文/空白保留、返回 str。
- 主会话在共享项目独立运行 `python3 -B -m unittest -v`：exit 0，4 项全部通过。此证据证明两个本地函数契约；不涉及外部服务或模型能力。

## 产物版本

- `normalize.py` SHA256 `82de932714d81c26041527c30651ee3801d0ec2d9fd26fa923d5a37fb617814d`
- `render.py` SHA256 `83ac337e7a4e55cbcd34e5e65b7112e6475ed978ca344ac12d999bfcb5440031`
- `test_tools.py` SHA256 `83c215445e10d9c9281c7ac78ab7672e7e853b08eed0ddaed0f1713c39fb3e97`

## 收口与资源

业务实现与边界验证完成。计划的派单、判据、结果已保存于本文件，活动计划可移除。无剩余产品阻塞。主会话没有内部 Agent 归档/结束工具，未执行或声称执行该生命周期操作；执行者均报告无在途进程/临时资源，宿主生命周期由上层管理。无工作树需要删除。非 Git 项目，未安装、commit、push。
