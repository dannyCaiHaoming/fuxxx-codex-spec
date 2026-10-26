# 订单重复接收修复

## 已确认目标与方案

依据 `contract.md`：event_id 标识同一事件；重复接收不再重复存储；不同 order_id 即使金额相同也保留；原始导出与列表均读 store；不得清理未知历史。

链路为 events.json → app.py 导出的 receive → store → 原始读取／list_orders。原实现 receive 无条件追加每次投递的副本，导致 e1 存储两次。只在列表过滤只能遮住显示症状，原始导出仍重复，不满足契约。修复在可控的接收边界按 event_id 查找已有记录，存在即返回，否则保留原复制追加逻辑。list_orders 不需更改。

本次走轻量路径：复现原始输入 → 修改接收边界 → 验证原始存储及列表、重复重放和历史保留 → 将方案和证据保存在本文件。无需独立 MVP、临时 plan 或 handoff；无剩余实施任务。

## 实际差量

- orders.py：receive 增加读取事件标识及已有标识检查，共 3 行；其他实现不变。
- test_orders.py：新增 5 个标准库测试，经 app.py 导出的函数执行。
- repair-notes.md：本次方案、证据及限制。
- AGENTS.md、contract.md、app.py、events.json 保持原样。目录没有 Git 元数据，无提交、推送、安装或委派。

## 实际验证与证据

环境：Python 3.13.10。命令：`python3 -B -m unittest -v test_orders`。

同一测试文件先针对原实现执行：5 项中 3 项失败，覆盖原始事件重复、已存事件重收、历史记录后重收。修改后再次执行：5 项全部通过。其余测试验证相同金额不同订单保留及输入／列表副本隔离。

另经 app.py 读取真实 events.json 顺序调用 receive 并直接检查 store 与 list_orders，两者实际均为：

```json
[{"event_id":"e1","order_id":"o1","amount":10},{"event_id":"e2","order_id":"o2","amount":10}]
```

测试中的整批再次投递也保持相同结果。历史重复记录和无 event_id 的历史字典保持原样，没有实施后果清理。

验证版本 SHA-256：

- orders.py：f1592dfe4e960e1ef7a42aca286e31c0943fcbb6a14838055437cb7bf3bad8c5
- test_orders.py：29053d3343d77ca35132a04aa7ac4ae5063c935788cd55456bd3d2170a858e4a
- events.json：90307beb24420d34a84df0e2d5e0ff553f7c4306260c4b8e5b8ea70655f28097

## 完成边界

本地顺序接收链路的重复存储原因已修复；这是自检与真实样例函数链路验证，未作独立评审。项目仅有内存列表及导入入口，没有独立导出程序；原始导出依据契约以直接读取 store 验证。没有声称数据库、并发、多进程或外部服务验收。

接收输入沿用契约中具有稳定 event_id 的事件，同一标识保留首次接收内容；未定义缺失标识或冲突载荷的新业务处理。本实现每次线性扫描 store，适用当前小型内存项目。已有历史重复不自动修复，避免违反禁止清理要求；当前证明的是防止接收再增重，不是任意历史存储必然唯一。
