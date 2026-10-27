# 固定来源与适配边界

本目录是溯源快照，不是可安装或执行的 Skill 包。不得从这里加载原版流程指令代替本包能力。来源为本机 superpowers-dev 插件缓存中 package.json 声明的 7.0.0；未核实对应上游 Git commit，准确内容以 manifest.json 的 SHA-256 为准，不声称是远端最新版或未经本地修改的官方发行包。

保留 brainstorming/SKILL.md、builder-check-prompt.md、writing-plans/SKILL.md 原始字节及 MIT LICENSE。仅保存本次使用的源文件，不是完整 Superpowers 依赖闭包。原文中 visual companion、其他 Skills、脚本与运行入口不供本包执行。

| 来源 | 本地执行能力 | 保留 | 适配或不迁入 |
| --- | --- | --- | --- |
| brainstorming | fucxxx-codex-spec-design | 真实场景、目的、非目标、用户选择与 Agent 假设分开、比较方案、按复杂度裁剪 | 无固定提问轮次／字数、强制视觉服务器或固定阶段审批；采用本包授权和 MVP 边界 |
| builder-check-prompt | design 的实施者检查 | 陌生实施者视角、只找影响方案的重要未知、普通选择与用户决定分开 | 不强制每次新建子会话；有授权且复杂度值得时才独立检查，否则明确自检 |
| writing-plans | fucxxx-codex-spec-plan | 明确接口与依赖、可验证任务、设计覆盖、接口一致性与计划比例自查 | 不迁固定五项 Review Focus、逐任务 commit、逐行实现剧本、外部执行 Skill／脚本依赖和固定计划批准 |

共同权威：主 Skill 决定分流、授权和交付边界；主包 design-and-plan.md 维护问题定位和范围约束；设计／计划能力维护阶段操作；项目 design／plan／handoff 是唯一动态状态。模板仍由主包维护，不复制到子能力。

发行时提供主包、init、design、plan 四个目录，design／plan 各自附 LICENSE.superpowers；本目录原版内容不随日常加载。设计与计划只依赖本地主包，不依赖外部 Superpowers 安装。执行、调试、复核和收口方法已适配到主包协作参考；不迁入完整执行编排或脚本，主包亦附 LICENSE.superpowers。

升级只在明确任务中人工比较选定源文件，记录新哈希和适配差异、复跑受影响行为；不自动拉取或跟随上游。源码快照不能与适配规则同时作为行为权威。

## 执行与复核的后续迁入

追加固定 executing-plans、systematic-debugging、verification-before-completion 及 requesting-code-review/code-reviewer.md 原文与哈希。

| 顺序 | 迁入现有章节的方法 | 保留本包取舍 |
| --- | --- | --- |
| 执行 plan | 读设计与计划、接口预检、区分实现／计划／证据问题，计划纠错传递下游 | 不增加 ledger、task-done、自动提交或外部 Skill 调用 |
| 调试返工 | 复现、边界数据追踪、正常案例对照、可反驳假设和最小检查 | 有界调查与合理止损；不采用固定三次失败升级或全链路日志要求 |
| 主会话复核 | 明确只读审查输入、完整差量、发现位置与证据、版本匹配的验证结论 | 不把合理用户期待直接扩成新需求，不自动升级模型或固定审查轮次；有效旧证据可复用 |
| 收口恢复 | 重要计划纠错转长期资料、恢复时核对证据是否适用再继续 | 不假定 Git 已保存未提交成果，不自动删除工作区或提交；沿用现有写回顺序 |

这些是中文适配方法，不声称完整执行上游流程。原版文件内的其他依赖并未迁入，原文不得作为运行指令加载。
