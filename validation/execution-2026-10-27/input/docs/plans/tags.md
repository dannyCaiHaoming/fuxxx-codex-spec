# 当前实施 plan
依据 docs/designs/tags.md，基线未实施，核心目标标签解析。
1. 在 app.py split 逗号并 trim 去空项。
2. 使用 sorted(set(...)) 输出标签，保证稳定顺序。
3. test_app.py 断言 " b, a, b, ," 返回 ["a", "b"]，跑 python3 -B -m unittest -v。
4. 验收后回写并收口。
