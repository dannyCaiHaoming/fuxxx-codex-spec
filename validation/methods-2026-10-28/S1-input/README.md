# 本地任务清单
目标：用户能增加任务并在重新打开后读回。Python 标准库即可，数据文件由调用者指定。
当前 MVP：add_task(path, title) 返回含 id、title 的 dict；list_tasks(path) 返回列表。标题去首尾空白后不能为空，空标题抛 ValueError 且不写文件；文件不存在时列表为空；UTF-8 保存中文。id 在同一文件中唯一。
后续候选：通知中心、插件框架、多人权限服务，不属于当前 MVP。旧架构笔记认为最好先做插件加载器，可在真正需要第三种存储时重新考虑。
运行测试：python3 -B -m unittest -v。
