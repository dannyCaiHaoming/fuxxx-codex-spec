# 列表重复显示止损结果

依据：本项目 AGENTS.md、contract.md，以及指定包的 SKILL.md、references/design-and-plan.md、references/collaboration-and-closeout.md。读取了 app.py、orders.py、events.json；未访问其他样例或真实仓库。本目录无 .git，未向上查找仓库；原始相关文件以 SHA-256 核对保留情况。

## 方案与范围

现有链路是 app 导入 receive / list_orders，receive 逐次追加到 store，列表逐行复制。原始 events.json 有两条 e1，基线运行得到 store 3 条、列表 3 条（e1/e1/e2）。原因明确：重复投递仍存储且未经展示过滤。

遵照已确认 contract.md，仅修改 list_orders：按 event_id 保留首次出现，保持顺序，返回行副本；无标识、null 或空标识的历史行保留，避免凭金额猜测身份。不同事件即使金额相同也保留。此小项目使用相等比较记录已见标识，避免额外限定 ID 类型；最坏二次复杂度，未进行大数据性能验收。

不选择修改 receive，因为它是不可修改的供应商镜像；不清理 store，因为原始导出和历史保留是明确约束。这是列表展示止损，未消除供应商重复投递原因，未恢复历史账务正确性。

## 差量

- orders.py：只修改 list_orders；receive 原文保持。
- test_orders.py：新增可复跑的标准库测试。
- RESULT.md：本次轻量方案、验证和限制记录。没有新建设计体系、活动 plan 或接入声明。

## 实际验证

2026-10-27，在本项目执行 `python3 -B -m unittest -v test_orders`，3 项测试全部通过：原始输入经 app 导出入口接收与列表读取；相同金额的不同订单及不相邻重复；未知历史数据和空列表。测试同时验证 store 不变、模拟原始 JSON 导出不变、返回行的顶层修改不会影响 store。

最终同次直接运行原始输入：raw_count=3，list_count=2，列表为 e1/o1/10 与 e2/o2/10。另以基线 hash 确认 AGENTS.md、contract.md、app.py、events.json 未变，并逐字确认 receive 未变。

最终 orders.py SHA-256：`8e40c8ea77c91299642af20b60e4f7ddc6794eaf21eb2d85b368081fb6e1c8e7`。未安装依赖、未 commit/push、未委派，无在途进程。验证是本地真实函数链路自检，不是独立评审或生产界面验收。

## 剩余风险与重新处理条件

原始 store 及其导出仍含重复事件；依赖它们的金额汇总或对账可能重复计数。本轮不承诺对账准确性，也没有真实导出模块可运行验收。列表按同一事件首次记录展示，不裁决同 ID 不同内容的正确版本。缺失稳定标识的历史记录不会被合并。

供应商下周可处理后，应另行明确源头幂等接收及对账修复的授权与验收；历史清理需单独确认，不能从本次展示止损推导授权。本轮已达到约定展示止损终点，不扩展其他业务。
