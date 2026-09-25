#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把贡献蛇 SVG 以 base64 data URI 内联进 README,彻底避免外部图片请求。

背景：raw.githubusercontent.com 在中国大陆访问不稳定且不被 GitHub camo 代理,
导致 profile README 里的 snake 图经常破图。改为 base64 内联后,
图片随 README 一起由 github.com 分发,任何网络都能正常显示,不再依赖第三方托管。

用法：
    python3 scripts/embed_snake.py [svg_path] [readme_path]
    svg_path   默认 github-contribution-grid-snake-dark.svg
    readme_path 默认 README.md
"""

import base64
import os
import sys

# 内联段标记:脚本仅替换两个标记之间的内容,其它部分保持不变
MARKER_OPEN = "<!-- SNAKE-DATA-URI -->"
MARKER_CLOSE = "<!-- /SNAKE-DATA-URI -->"


def data_uri(svg_path: str) -> str:
    """读取 SVG 文件并返回 base64 data URI 字符串。"""
    with open(svg_path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode("ascii")
    return "data:image/svg+xml;base64," + b64


def embed(readme_path: str, svg_path: str) -> bool:
    """用 data URI 替换 README 中两个标记之间的 snake 图片段。

    返回 True 表示发生了替换,False 表示未找到标记或内容未变化。
    """
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(MARKER_OPEN)
    end = content.find(MARKER_CLOSE)
    if start == -1 or end == -1:
        print(f"[embed_snake] 未找到标记 {MARKER_OPEN}/{MARKER_CLOSE},跳过", file=sys.stderr)
        return False

    # data URI 会随 snake SVG 的像素内容一起出现在 README 里
    uri = data_uri(svg_path)
    block = (
        f"{MARKER_OPEN}\n"
        f'<img src="{uri}" alt="GitHub Contribution Snake" width="880" />\n'
        f"{MARKER_CLOSE}"
    )

    new_content = content[:start] + block + content[end + len(MARKER_CLOSE):]
    if new_content == content:
        print("[embed_snake] snake 内容无变化,无需更新")
        return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[embed_snake] 已内联 {os.path.basename(svg_path)} -> {readme_path} "
          f"({len(uri)} 字符)")
    return True


def main() -> int:
    readme_path = sys.argv[2] if len(sys.argv) > 2 else "README.md"
    svg_path = sys.argv[1] if len(sys.argv) > 1 else "github-contribution-grid-snake-dark.svg"
    embed(readme_path, svg_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())