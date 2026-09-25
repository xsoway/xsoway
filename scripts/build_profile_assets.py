"""Generate GitHub-safe Gruvbox SVG text panels for the profile README."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "Arial, PingFang SC, Microsoft YaHei, sans-serif"
MONO = "Menlo, Consolas, monospace"

PROJECTS = [
    ("codebase-graph-prd-rules", 13, "从代码生成可追溯的业务规则", "Traceable business rules from code"),
    ("locust-perf-framework", 3, "压测方案、执行数据与中文报告", "Test plans, run data, and Chinese reports"),
    ("skill-spec", 2, "Codex Skill 包的工程规范", "Engineering standards for Codex Skills"),
    ("oss-release-prep", 1, "开源发布检查与双语 README", "Release checks and bilingual READMEs"),
    ("obsidian-ai-vault-scaffold", 1, "Obsidian Vault 骨架与自动化", "Obsidian Vault scaffold and automation"),
    ("echo-me-skill", 1, "可运行的数字自画像 Skill", "A runnable digital self portrait Skill"),
    ("wx_upload_cover_tool", 1, "公众号封面生成工具", "Cover image generator for WeChat"),
    ("llm-wiki-knowledge-vault", 1, "LLM Wiki 知识库工具", "Tools for an LLM Wiki knowledge base"),
    ("editor-html", 1, "面向产研测的 HTML 编辑器", "HTML editor for product, engineering, QA"),
]


def svg(name: str, width: int, height: int, body: str) -> None:
    if name.startswith("project-"):
        frame = f'<rect width="{width}" height="{height}" fill="#282828"/><path d="M0 {height-1}H{width}" stroke="#50493c"/>'
    else:
        frame = (
            f'<rect width="{width}" height="{height}" rx="12" fill="#1d2021"/>'
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="11.5" '
            'fill="none" stroke="#50493c"/>'
        )
    output = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">{frame}{body}</svg>\n'
    )
    (ASSETS / name).write_text(output, encoding="utf-8")


def label(x: int, y: int, value: str, size: int, color: str, *, mono: bool = False, weight: int = 400) -> str:
    face = MONO if mono else FONT
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" font-family="{face}">{escape(value)}</text>'
    )


def build_about(lang: str) -> None:
    if lang == "zh":
        lines = [
            ("把 AI 的能力做成可验证、可复用的工具。", "#d8a657", 23, 77),
            ("我是 Alan Hsu，一名测试开发工程师。", "#ebdbb2", 19, 119),
            ("持续研究 AI Agent、Skills 和个人知识工具。", "#ebdbb2", 19, 152),
            ("01 / 我在做什么", "#d8a657", 21, 207),
            ("AI AGENTS", "#a9b665", 16, 247),
            ("TEST ENGINEERING", "#a9b665", 16, 279),
            ("KNOWLEDGE TOOLS", "#a9b665", 16, 311),
        ]
        detail = ["可组合、可执行的工作流", "性能测试与有证据的分析", "连接阅读、笔记与写作"]
    else:
        lines = [
            ("Practical. Verifiable. Reusable.", "#d8a657", 25, 77),
            ("I'm Alan Hsu, a test development engineer.", "#ebdbb2", 18, 119),
            ("I explore AI agents, Skills, and knowledge tools.", "#ebdbb2", 18, 152),
            ("01 / WHAT I WORK ON", "#d8a657", 21, 207),
            ("AI AGENTS", "#a9b665", 16, 247),
            ("TEST ENGINEERING", "#a9b665", 16, 279),
            ("KNOWLEDGE TOOLS", "#a9b665", 16, 311),
        ]
        detail = ["Composable workflows", "Performance and evidence", "Reading, notes, writing"]
    body = label(26, 33, "ALAN / PROFILE", 13, "#a89984", mono=True)
    body += '<path d="M26 48H534M26 176H534" stroke="#50493c"/>'
    for value, color, size, y in lines:
        body += label(26, y, value, size, color, mono=y >= 207, weight=700 if y in (77, 207) else 400)
    for value, y in zip(detail, (247, 279, 311)):
        body += label(221, y, value, 16, "#ebdbb2")
    svg(f"about-{lang}.svg", 560, 338, body)


def build_heading(lang: str, kind: str) -> None:
    titles = {
        ("zh", "projects"): ("02 / 精选项目", "PUBLIC · NON-FORK · STARS AS OF 2026-09-25"),
        ("en", "projects"): ("02 / SELECTED WORK", "PUBLIC · NON-FORK · STARS AS OF 2026-09-25"),
        ("zh", "contact"): ("03 / 在别处找到我", "BLOG · CODE · CONVERSATION"),
        ("en", "contact"): ("03 / FIND ME ELSEWHERE", "BLOG · CODE · CONVERSATION"),
    }
    title, subtitle = titles[(lang, kind)]
    body = '<path d="M24 72H536" stroke="#d79921" stroke-opacity=".55"/>'
    body += label(24, 43, title, 24, "#d8a657", weight=700)
    body += label(24, 64, subtitle, 11, "#a89984", mono=True)
    svg(f"{kind}-{lang}.svg", 560, 82, body)


def build_projects() -> None:
    for position, (name, stars, zh, en) in enumerate(PROJECTS, 1):
        for lang, description in (("zh", zh), ("en", en)):
            body = label(22, 30, f"{position:02}", 14, "#a89984", mono=True)
            body += label(62, 32, name, 22, "#d8a657", weight=700)
            body += label(62, 58, description, 16, "#ebdbb2")
            body += label(474, 31, f"★ {stars}", 16, "#a9b665", mono=True, weight=700)
            svg(f"project-{name}-{lang}.svg", 560, 70, body)


def build_buttons() -> None:
    for name, text, width in (
        ("zh", "中文", 96), ("en", "English", 110),
        ("blog", "BLOG ↗", 120), ("repos", "REPOS ↗", 130),
        ("x", "X ↗", 80), ("telegram", "TELEGRAM ↗", 160),
        ("email", "EMAIL ↗", 130),
    ):
        body = label(18, 31, text, 18, "#d8a657", mono=name not in ("zh", "en"), weight=700)
        svg(f"button-{name}.svg", width, 48, body)


def build_contact_details(lang: str) -> None:
    first = "公众号 / 自由的灵魂在路上 · xsoway" if lang == "zh" else "WeChat public account / 自由的灵魂在路上 · xsoway"
    body = label(22, 39, first, 17, "#ebdbb2")
    body += label(22, 73, "WECHAT / Alan_Hsu_521", 17, "#d8a657", mono=True)
    body += '<path d="M22 93H538" stroke="#50493c"/>'
    body += label(22, 122, "离开乏味的皮囊，自由的灵魂在路上", 16, "#a89984")
    svg(f"contact-details-{lang}.svg", 560, 143, body)


def build_readme(lang: str) -> None:
    title = "我的开源项目，按 GitHub Star 数排序" if lang == "zh" else "My open source projects, sorted by GitHub stars"
    about = "Alan Hsu：测试开发、AI Agent、Skills 和个人知识工具" if lang == "zh" else "Alan Hsu: test engineering, AI agents, Skills, and knowledge tools"
    lines = [
        '<div align="center">',
        '  <picture>',
        '    <source media="(max-width: 600px)" srcset="./assets/hero-mobile.svg" />',
        '    <img src="./assets/hero.svg" alt="Alan Hsu — Test engineering, AI agents, and knowledge systems" width="560" />',
        '  </picture>',
        '  <br />',
        '  <a href="./README.md"><img src="./assets/button-zh.svg" alt="中文" width="96" /></a>',
        '  <a href="./README.en.md"><img src="./assets/button-en.svg" alt="English" width="110" /></a>',
        f'  <br /><img src="./assets/about-{lang}.svg" alt="{about}" width="560" />',
        f'  <br /><img src="./assets/projects-{lang}.svg" alt="{title}" width="560" />',
    ]
    for name, stars, zh, en in PROJECTS:
        description = zh if lang == "zh" else en
        lines.append(
            f'  <br /><a href="https://github.com/xsoway/{name}">'
            f'<img src="./assets/project-{name}-{lang}.svg" '
            f'alt="{name}: {description}; {stars} {"star" if stars == 1 else "stars"}" width="560" /></a>'
        )
    lines += [
        f'  <br /><img src="./assets/contact-{lang}.svg" alt="Contact and links" width="560" />',
    ]
    contacts = [
        ("blog", "https://xsoway.github.io", "Blog"),
        ("repos", "https://github.com/xsoway?tab=repositories", "All repositories"),
        ("x", "https://x.com/AlanHsu521", "X"),
        ("telegram", "https://t.me/AlanHsu521", "Telegram"),
        ("email", "mailto:xulanzhong521@gmail.com", "Email"),
    ]
    for name, url, label_text in contacts:
        lines.append(
            f'  <a href="{url}"><img src="./assets/button-{name}.svg" alt="{label_text}" /></a>'
        )
    lines += [
        f'  <br /><img src="./assets/contact-details-{lang}.svg" '
        'alt="WeChat public account: 自由的灵魂在路上, xsoway; WeChat: Alan_Hsu_521" width="560" />',
        '</div>',
    ]
    destination = ROOT / ("README.md" if lang == "zh" else "README.en.md")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for language in ("zh", "en"):
        build_about(language)
        build_heading(language, "projects")
        build_heading(language, "contact")
    build_projects()
    build_buttons()
    for language in ("zh", "en"):
        build_contact_details(language)
        build_readme(language)
