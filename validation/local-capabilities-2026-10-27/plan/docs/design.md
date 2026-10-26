# 已确认设计

本地单用户任务标题工具，Python 标准库。normalize_title(title: str) -> str 应去首尾空白，内部空格不变；空或纯空白抛 ValueError("empty title")。不增加服务、登录、分类或数据持久化。

只改 app.py 的函数并在 test_app.py 验证，测试入口 python3 -B -m unittest -v。当前不实施，先交付 plan。
