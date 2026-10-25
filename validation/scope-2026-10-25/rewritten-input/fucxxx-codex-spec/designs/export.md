# CSV MVP v2
当前验收：必须通过 OutputPolicy 拒绝绝对路径；每次失败后永久禁用该目标路径；并发锁和 WriterRegistry 为导出前置。然后覆盖 CSV 特殊字符和空列表。
范围扩展理由：都与导出可靠性有关。
