# 标题工具
当前 MVP 提供两个独立函数：normalize_title 在 normalize.py，strip 后非空，否则 ValueError；render_title 在 render.py，将标题 HTML 转义，包含 & < > 双引号和单引号，返回 str。不引入插件、HTTP 服务、配置引擎。标准库即可。运行 python3 -B -m unittest -v。
