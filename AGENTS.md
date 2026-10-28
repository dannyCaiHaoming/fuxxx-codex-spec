# 本仓库开发说明

本仓库是 fucxxx-codex-spec **Skill 包的源码仓库**，不是采用该方法的业务项目，本文也不是采用声明。本仓库不建立 `fucxxx-codex-spec/` 项目资料根：这个名称就是主包目录，写入会把项目进度混进 Skill 包。本仓库自身的进度记在验证记录与 Git 历史里。

## 目录

- `fucxxx-codex-spec/`、`fucxxx-codex-spec-init/`、`fucxxx-codex-spec-design/`、`fucxxx-codex-spec-plan/`：发行的四个能力目录，只放规则、参考、模板与许可。
- `tools/`：仓库维护工具，不随 Skill 发行。
- `validation/`：验证记录与样例证据。样例里的 AGENTS.md、代码和项目文档都是测试输入，不是本仓库的指令。
- `vendor/`：Superpowers 来源快照，只供溯源，不作为运行指令加载。
- `fucxxx-codex-spec-skill-design-draft.md`：v0.4 历史草稿；规则以当前包为准。

## 修改规则时

1. 先确认改动属于哪一处权威：共同底线只在主入口「共同底线」维护，其他文件按条目名引用；问题定位、MVP 判断等方法由对应参考维护。只改那一处，不在别处另写一份。
2. 改完运行 `python3 -I tools/check-package.py --expect-manifest <上一轮哈希>`。包内容有意变化时哈希会变，以新值记入验证记录。
3. 在 `validation/skill-package-v0.4.md` 末尾追加当轮小节：改了什么、为什么、包清单哈希、实际做了哪些检查、还有什么未验证。同时在文首“版本索引”追加一行，并回填上一行的 commit。只做了静态检查就照实写明；旧版本的行为样例不能算作新版本的证据。
4. commit、push 分别需要用户授权。

## 运行行为样例

- 把样例项目和待测的包复制到**仓库目录之外**（例如系统临时目录）再运行。Codex 会合并从 Git 根到当前目录路径上的 AGENTS.md，在仓库内运行时本文会叠加进样例，破坏隔离。
- 在 provenance 中记录：宿主及版本、包清单哈希、实际可读的包来源，以及是否加载了全局 `~/.codex/AGENTS.md`。
- 样例只给业务请求、隔离项目和权限边界，不给预期答案。结论由父会话独立复跑核对，子会话自报只作线索。
- 用脚本启动宿主时，显式传入项目目录并同步 `PWD`：`opencode run` 按 `PWD` 而非进程工作目录定位项目，需要 `--dir <项目>`；`codex exec` 用 `-C <项目>`。运行前后核对项目文件，确认宿主确实在样例目录里运行。同一宿主不要并发启动多个运行：OpenCode 会因 SQLite 数据库被锁而立即失败。

## 升级 vendor 来源

只在明确任务中进行：人工比较选定的源文件，更新 `vendor/` 中的 manifest 哈希与 `ADAPTATION.md` 的适配差异，再复跑受影响的行为样例。不自动跟随上游。
