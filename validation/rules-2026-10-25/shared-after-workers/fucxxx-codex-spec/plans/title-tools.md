# 标题工具实施计划

## 0. 交接与写入归属

项目目录：/private/var/folders/tn/x1hbkfy17sx0w1lb8kjzzr340000gn/T/fucxxx-rules-a16h1b4c/shared

读取本项目 AGENTS.md、README.md、fucxxx-codex-spec/design.md 和本计划。Skill 入口：/Users/caihaoming/Documents/fuxxx-codex-spec/fucxxx-codex-spec/SKILL.md。方案版本：本轮 design.md；所有文件都未提交。仅本项目内离线标准库操作，不安装、commit、push，不修改外部 Skill，不读取其他样例。

- `README.md` SHA256: `45a2bee5cf5edafba9916090ff4ddcf7026195f7ea26dcfbe90f3b82029b4e7b`
- `normalize.py` SHA256: `fbe6d9b3bebc7ad2688f0e055bc383d4d67dbe37055278b103ee13e11e3ccebf`
- `render.py` SHA256: `06f532703863fee3a70d57aeb9d4cfcd4489aaaffaab291956919498089f838d`
- `test_tools.py` SHA256: `33244271e7c8eecbee2754e6b7397fe981c017f16e3550eaffaccaf3d197770f`

两名内部子 Agent 共用当前目录；normalize 执行者仅可写 normalize.py；render 执行者仅可写 render.py。两人均不得改共享 test_tools.py、设计、计划或 handoff。执行结果通过返回消息交主会话；主会话是本计划唯一维护者，负责测试增强与最终文档。若需修改对方文件，先返回证据，不越界写入。

## 1. normalize 派单正文（待实际派发）

按 §0 读取依据，仅在 normalize.py 实现 normalize_title：strip 后非空返回，空值抛 ValueError。保留函数名及独立职责。运行 `python3 -B -m unittest -v test_tools.Tools.test_normalize`，额外检查空字符串和 Unicode 空白。返回实际差量、验证命令和结果、限制及资源状态，不自行收口主区文档。

## 2. render 派单正文（待实际派发）

按 §0 读取依据，仅在 render.py 实现 render_title：标准库 HTML 转义 & < > 双引号和单引号，返回 str。不要增加 normalize 依赖。运行 `python3 -B -m unittest -v test_tools.Tools.test_render`，额外检查普通文本、完整五种字符、空字符串和返回类型。返回实际差量、验证命令和结果、限制及资源状态，不自行收口主区文档。

## 3. 主会话复核与收口

读取两名子 Agent 的结果，审阅实际文件差量，补充必要边界测试，运行 README 全量命令。只有实际通过才回写 design.md、handoff.md，保留验收证据并移除本计划。禁止把预备派单称为已经派发。

## 实际执行记录

- 主会话：已读取项目规则、README、代码、测试及指定 Skill 和两份参考。
- 初始验证：`python3 -B -m unittest -v`，exit 1，两项测试均因 NotImplementedError 报错。
- normalize：尚未派发，尚未修改。
- render：尚未派发，尚未修改。
- 环境限制：当前工具集合未暴露内部 spawn_agent/send_message/wait_agent 等工具；不是已确认的槽位占用，不能假称等待槽位就会恢复。
