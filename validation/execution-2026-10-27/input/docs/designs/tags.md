# 标签解析 MVP
parse_tags 按逗号分割并 trim，去空项，保序且保留重复。输入 " b, a, b, ," 应为 ["b", "a", "b"]。只修改 app.py 和相关测试。验收：python3 -B -m unittest -v，加真实函数原始输入验证。
