# 固定来源与适配边界

本目录是溯源快照，不是可安装或执行的 Skill 包。不得从这里加载原版流程指令代替本包能力。来源为本机 superpowers-dev 插件缓存中 package.json 声明的 7.0.0；未核实对应上游 Git commit，准确内容以 manifest.json 的 SHA-256 为准，不声称是远端最新版或未经本地修改的官方发行包。

保留 brainstorming/SKILL.md、builder-check-prompt.md、writing-plans/SKILL.md 原始字节及 MIT LICENSE。仅保存本次使用的源文件，不是完整 Superpowers 依赖闭包。原文中 visual companion、其他 Skills、脚本与运行入口不供本包执行。

| 来源 | 本地执行能力 | 保留 | 适配或不迁入 |
| --- | --- | --- | --- |
| brainstorming | fucxxx-codex-spec-design | 真实场景、目的、非目标、用户选择与 Agent 假设分开、比较方案、按复杂度裁剪 | 无固定提问轮次／字数、强制视觉服务器或固定阶段审批；采用本包授权和 MVP 边界 |
| builder-check-prompt | design 的实施者检查 | 陌生实施者视角、只找影响方案的重要未知、普通选择与用户决定分开 | 不强制每次新建子会话；有授权且复杂度值得时才独立检查，否则明确自检 |
| writing-plans | fucxxx-codex-spec-plan | 明确接口与依赖、可验证任务、设计覆盖、接口一致性与计划比例自查 | 不迁固定五项 Review Focus、逐任务 commit、逐行实现剧本、外部执行 Skill／脚本依赖和固定计划批准 |

共同权威：主 Skill 决定分流、授权和交付边界；主包 design-and-plan.md 维护问题定位和范围约束；设计／计划能力维护阶段操作；项目 design／plan／handoff 是唯一动态状态。模板仍由主包维护，不复制到子能力。

发行时提供主包、init、design、plan 四个目录，design／plan 各自附 LICENSE.superpowers；本目录原版内容不随日常加载。设计与计划只依赖本地主包，不依赖外部 Superpowers 安装。执行编排没有在本轮搬入，仅沿用已有协作方法。

升级只在明确任务中人工比较选定源文件，记录新哈希和适配差异、复跑受影响行为；不自动拉取或跟随上游。源码快照不能与适配规则同时作为行为权威。
