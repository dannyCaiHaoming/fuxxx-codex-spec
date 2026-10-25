from html import escape


def render_title(title):
    return escape(title, quote=True)
