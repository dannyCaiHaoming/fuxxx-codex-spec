#!/usr/bin/env python3
"""fucxxx-codex-spec Skill 包的结构检查与包清单哈希。

把历来每轮验证手工重做的检查固定成一处可复跑实现：包结构、YAML 元数据、
Markdown 围栏、本地链接、Git 空白诊断、vendor 来源哈希，以及包清单 SHA-256。

只读检查，不修改仓库；唯一写入是显式 --write-manifest 指定的清单文件。
不安装依赖：标准库即可运行；有 ruby 时用 Psych 做真正的 YAML 解析，
没有则退回内置最小解析器，并在报告里注明用了哪一个——不把退回当成官方校验通过。

用法：
    python3 -I tools/check-package.py
    python3 -I tools/check-package.py --scope repo
    python3 -I tools/check-package.py --expect-manifest <sha256>
    python3 -I tools/check-package.py --write-manifest validation/<轮次>/package-manifest.json
    python3 -I tools/check-package.py --json

退出码：0 全部通过（含仅警告）；1 有失败项；2 用法或环境错误。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

# 发行时提供的四个能力目录；顺序只影响报告，不影响清单哈希（清单按路径排序）。
PACKAGES = [
    "fucxxx-codex-spec",
    "fucxxx-codex-spec-init",
    "fucxxx-codex-spec-design",
    "fucxxx-codex-spec-plan",
]

# 两种范围都检查的仓库根文档。
ROOT_ENTRY_DOCS = ["README.md", "AGENTS.md"]
# 仓库范围检查时另外纳入的顶层文档。
ROOT_DOCS = ["fucxxx-codex-spec-skill-design-draft.md"]

VENDOR_MANIFEST = "vendor/superpowers-7.0.0/manifest.json"

# 故意保留的断链：init 样例刻意不提供主入口，用于验证"主入口不可用"分支。
# 键是相对仓库根的文件，值是该文件中允许解析失败的链接目标。
ALLOWED_BROKEN_LINKS = {
    "validation/init-and-cause-2026-10-27/missing/available/"
    "fucxxx-codex-spec-init/SKILL.md": {"../fucxxx-codex-spec/SKILL.md"},
    "validation/init-and-cause-2026-10-27/inputs/missing/available/"
    "fucxxx-codex-spec-init/SKILL.md": {"../fucxxx-codex-spec/SKILL.md"},
}

LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


class Report:
    """收集检查结果；failures 决定退出码，warnings 只提示。"""

    def __init__(self) -> None:
        self.checks: list[dict] = []
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def add(self, name: str, ok: bool, detail: str, **extra) -> None:
        entry = {"check": name, "ok": ok, "detail": detail}
        entry.update(extra)
        self.checks.append(entry)
        if not ok:
            self.failures.append(f"{name}: {detail}")

    def warn(self, name: str, detail: str) -> None:
        self.warnings.append(f"{name}: {detail}")
        self.checks.append({"check": name, "ok": True, "warning": detail})


def repo_root() -> str:
    """以脚本位置推定仓库根，不依赖调用时的 cwd。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_files(root: str, rel_dir: str) -> list[str]:
    """返回 rel_dir 下全部文件的仓库相对路径，跳过 .DS_Store 之类噪声。"""
    found = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(root, rel_dir)):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name == ".DS_Store":
                continue
            abs_path = os.path.join(dirpath, name)
            found.append(os.path.relpath(abs_path, root))
    return sorted(found)


# --- 1. 包结构 -------------------------------------------------------------


def check_structure(root: str, report: Report) -> list[str]:
    """确认四个能力目录存在且各有 SKILL.md；返回包内全部文件。"""
    all_files: list[str] = []
    missing = []
    for pkg in PACKAGES:
        if not os.path.isdir(os.path.join(root, pkg)):
            missing.append(pkg)
            continue
        files = walk_files(root, pkg)
        all_files.extend(files)
        if f"{pkg}/SKILL.md" not in files:
            missing.append(f"{pkg}/SKILL.md")
    if missing:
        report.add("structure", False, "缺少：" + "、".join(missing))
    else:
        per_pkg = {p: sum(1 for f in all_files if f.startswith(p + "/")) for p in PACKAGES}
        report.add(
            "structure",
            True,
            f"{len(PACKAGES)} 个能力目录齐全，共 {len(all_files)} 个文件",
            files_per_package=per_pkg,
        )
    return sorted(all_files)


# --- 2. YAML frontmatter ---------------------------------------------------


def split_frontmatter(text: str) -> str | None:
    """取出首个 --- 块的内容；没有则返回 None。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end].strip("\n")


def parse_frontmatter_ruby(path: str) -> dict | None:
    """用 Ruby Psych 解析，必须带 -E UTF-8，否则中文 frontmatter 会报
    invalid byte sequence in US-ASCII。"""
    ruby = shutil.which("ruby")
    if not ruby:
        return None
    script = (
        'require "yaml"; require "json";'
        't = File.read(ARGV[0], encoding: "UTF-8");'
        'raise "no frontmatter" unless t.start_with?("---");'
        'fm = t.split(/^---\\s*$/)[1];'
        "print JSON.generate(YAML.safe_load(fm))"
    )
    try:
        out = subprocess.run(
            [ruby, "-E", "UTF-8", "-e", script, path],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return {"__error__": (out.stderr or "").strip().splitlines()[:1]}
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return None


def parse_frontmatter_min(fm_text: str) -> dict:
    """内置最小解析器：只认顶层 `key: value`，够本包元数据使用。
    这不是 YAML 实现，报告里会注明用的是退回路径。"""
    data: dict[str, str] = {}
    key = None
    for line in fm_text.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip().strip("\"'")
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def check_frontmatter(root: str, report: Report) -> None:
    parser_used = "ruby-psych"
    rows = []
    problems = []
    for pkg in PACKAGES:
        path = os.path.join(root, pkg, "SKILL.md")
        if not os.path.isfile(path):
            continue
        text = open(path, encoding="utf-8").read()
        fm_text = split_frontmatter(text)
        if fm_text is None:
            problems.append(f"{pkg}/SKILL.md 没有 frontmatter")
            continue
        data = parse_frontmatter_ruby(path)
        if data is None:
            parser_used = "builtin-minimal"
            data = parse_frontmatter_min(fm_text)
        elif "__error__" in data:
            problems.append(f"{pkg}/SKILL.md YAML 解析失败：{data['__error__']}")
            continue
        name = (data.get("name") or "").strip()
        desc = (data.get("description") or "").strip()
        if name != pkg:
            problems.append(f"{pkg}/SKILL.md 的 name 是 {name!r}，与目录名不一致")
        if not desc:
            problems.append(f"{pkg}/SKILL.md 的 description 为空")
        elif len(desc) > 1024:
            problems.append(f"{pkg}/SKILL.md 的 description 超过 1024 字符（{len(desc)}）")
        rows.append({"package": pkg, "name": name, "description_chars": len(desc)})
    if parser_used == "builtin-minimal":
        report.warn(
            "frontmatter.parser",
            "未找到可用的 ruby，使用内置最小解析器；这不等于通过真正的 YAML 解析器，"
            "报告时不要写成官方校验通过",
        )
    if problems:
        report.add("frontmatter", False, "；".join(problems), parser=parser_used, entries=rows)
        return
    lengths = "、".join(f"{r['package']} {r['description_chars']}" for r in rows)
    report.add(
        "frontmatter",
        True,
        f"{len(rows)} 份 SKILL.md 的 name 与目录名一致，description 非空且在 1024 内（{lengths}）",
        parser=parser_used,
        entries=rows,
    )


# --- 3. 围栏与 4. 链接 -----------------------------------------------------


def md_files(root: str, scope: str) -> list[str]:
    files: list[str] = []
    for pkg in PACKAGES:
        files += [f for f in walk_files(root, pkg) if f.endswith(".md")]
    for doc in ROOT_ENTRY_DOCS:
        if os.path.isfile(os.path.join(root, doc)):
            files.append(doc)
    if scope == "repo":
        for doc in ROOT_DOCS:
            if os.path.isfile(os.path.join(root, doc)):
                files.append(doc)
        for extra in ("validation", "vendor"):
            if os.path.isdir(os.path.join(root, extra)):
                files += [f for f in walk_files(root, extra) if f.endswith(".md")]
    return sorted(set(files))


def check_fences(root: str, files: list[str], report: Report) -> None:
    problems = []
    for rel in files:
        text = open(os.path.join(root, rel), encoding="utf-8").read()
        opens = [i for i, line in enumerate(text.splitlines(), 1) if FENCE_RE.match(line)]
        if len(opens) % 2:
            problems.append(f"{rel} 围栏数为奇数（{len(opens)}），最后一处在第 {opens[-1]} 行")
    if problems:
        report.add("fences", False, "；".join(problems))
    else:
        report.add("fences", True, f"{len(files)} 个 Markdown 文件的围栏成对")


def slugify(text: str) -> str:
    """GitHub 风格锚点：小写、空格转连字符、去掉标点，保留中文。"""
    text = re.sub(r"[`*_~\[\]()]", "", text.strip().lower())
    text = re.sub(r"[^\w一-鿿\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def headings(path: str) -> set[str]:
    out = set()
    in_fence = False
    for line in open(path, encoding="utf-8").read().splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.add(slugify(m.group(2)))
    return out


def check_links(root: str, files: list[str], report: Report) -> None:
    total = 0
    broken = []
    expected_broken = 0
    bad_anchors = []
    for rel in files:
        path = os.path.join(root, rel)
        allowed = ALLOWED_BROKEN_LINKS.get(rel, set())
        for m in LINK_RE.finditer(open(path, encoding="utf-8").read()):
            target = m.group(1)
            if target.startswith(SKIP_LINK_PREFIXES):
                continue
            total += 1
            file_part, _, anchor = target.partition("#")
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(resolved):
                if target in allowed:
                    expected_broken += 1
                elif f"{rel} -> {target}" not in broken:
                    broken.append(f"{rel} -> {target}")
                continue
            if anchor and resolved.endswith(".md"):
                if slugify(anchor) not in headings(resolved):
                    bad_anchors.append(f"{rel} -> {target}")
    detail = f"{total} 条本地链接目标全部存在"
    if expected_broken:
        detail += f"；另有 {expected_broken} 条样例故意保留的断链（已登记为预期）"
    if broken:
        report.add("links", False, f"{len(broken)} 条断链：" + "；".join(broken), total=total)
    else:
        report.add("links", True, detail, total=total, expected_broken=expected_broken)
    if bad_anchors:
        report.warn(
            "links.anchors",
            f"{len(bad_anchors)} 条锚点未匹配到标题（锚点规则因渲染器而异，仅提示）："
            + "；".join(bad_anchors),
        )


# --- 5. Git 空白诊断 -------------------------------------------------------


def check_whitespace_textual(root: str, files: list[str], report: Report, why: str) -> None:
    """没有 Git 工作树时的退回检查：行尾空白与 CR。提取出的包目录（以及
    validation 里的非 Git 样例）就是这种情况，不能因此跳过检查。"""
    diagnostics = []
    for rel in files:
        with open(os.path.join(root, rel), "rb") as fh:
            for lineno, raw in enumerate(fh.read().split(b"\n"), 1):
                line = raw.decode("utf-8", "replace")
                if line.endswith("\r"):
                    diagnostics.append(f"{rel}:{lineno}: CR 行尾")
                    line = line[:-1]
                if line and line != line.rstrip():
                    diagnostics.append(f"{rel}:{lineno}: 行尾空白")
    if diagnostics:
        report.add(
            "whitespace", False, f"{len(diagnostics)} 条诊断：" + "；".join(diagnostics[:10])
        )
    else:
        report.add("whitespace", True, f"{len(files)} 个文件无行尾空白或 CR（{why}）")


def check_whitespace(root: str, files: list[str], report: Report) -> None:
    """git diff --check 的退出码对"有差异"也用 1，所以只按是否有诊断行判定——
    这正是 2026-10-25 那轮误判为失败的地方。未跟踪文件用 --no-index 对比空输入。"""
    git = shutil.which("git")
    if not git:
        check_whitespace_textual(root, files, report, "未找到 git，改用文本检查")
        return

    def run(args: list[str]) -> tuple[int, str]:
        out = subprocess.run(
            [git, "-C", root] + args, capture_output=True, text=True, timeout=120
        )
        return out.returncode, (out.stdout + out.stderr).strip()

    code, _ = run(["rev-parse", "--is-inside-work-tree"])
    if code != 0:
        check_whitespace_textual(root, files, report, "不在 Git 工作树内，改用文本检查")
        return

    diagnostics: list[str] = []
    for args in (["diff", "--check"], ["diff", "--cached", "--check"]):
        _, text = run(args)
        if text:
            diagnostics += text.splitlines()

    code, text = run(["ls-files", "--others", "--exclude-standard", "-z"])
    untracked = [p for p in text.split("\0") if p] if code == 0 else []
    for rel in untracked:
        if rel in files or any(rel.startswith(p + "/") for p in PACKAGES):
            _, text = run(["diff", "--no-index", "--check", os.devnull, rel])
            if text:
                diagnostics += text.splitlines()

    if diagnostics:
        report.add("whitespace", False, f"{len(diagnostics)} 条诊断：" + "；".join(diagnostics[:10]))
    else:
        report.add(
            "whitespace",
            True,
            f"已跟踪改动与 {len(untracked)} 个未跟踪文件均无空白诊断（忽略仅表示有差异的退出码）",
        )


# --- 6. vendor 来源哈希 ----------------------------------------------------


def check_vendor(root: str, report: Report) -> None:
    manifest_path = os.path.join(root, VENDOR_MANIFEST)
    if not os.path.isfile(manifest_path):
        report.warn("vendor", f"没有 {VENDOR_MANIFEST}，跳过来源哈希核对")
        return
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    base = os.path.dirname(manifest_path)
    problems = []
    for rel, expected in sorted(manifest.get("files", {}).items()):
        path = os.path.join(base, rel)
        if not os.path.isfile(path):
            problems.append(f"{rel} 缺失")
            continue
        actual = sha256_file(path)
        if actual != expected:
            problems.append(f"{rel} 哈希不符（实际 {actual[:12]}…，清单 {expected[:12]}…）")
    if problems:
        report.add("vendor", False, "；".join(problems))
    else:
        report.add(
            "vendor",
            True,
            f"{len(manifest.get('files', {}))} 份来源文件与 manifest.json 的 SHA-256 一致"
            f"（declared_version {manifest.get('declared_version')}，上游 commit 未核实）",
        )


# --- 7. 包清单哈希 ---------------------------------------------------------


def package_manifest(root: str, files: list[str]) -> tuple[dict[str, str], str]:
    """清单算法（与历轮验证记录一致）：按仓库相对路径排序，每项写成
    "相对路径 + Tab + 文件 SHA-256 + 换行"，对合并后的 UTF-8 文本取 SHA-256。"""
    entries = {rel: sha256_file(os.path.join(root, rel)) for rel in sorted(files)}
    blob = "".join(f"{rel}\t{h}\n" for rel, h in entries.items())
    return entries, hashlib.sha256(blob.encode("utf-8")).hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="fucxxx-codex-spec 包结构检查与清单哈希",
        epilog="只读检查；--write-manifest 是唯一写入。",
    )
    ap.add_argument(
        "--scope",
        choices=["packages", "repo"],
        default="packages",
        help="packages（默认）只查四个能力目录与根目录 README、AGENTS.md；repo 另含草稿、validation 与 vendor 文档",
    )
    ap.add_argument("--expect-manifest", metavar="SHA256", help="核对包清单哈希是否为该值")
    ap.add_argument("--write-manifest", metavar="PATH", help="把逐文件哈希写成 JSON 清单")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果，便于存入验证证据")
    args = ap.parse_args(argv)

    root = repo_root()
    report = Report()

    pkg_files = check_structure(root, report)
    if not pkg_files:
        print("未找到任何能力目录，确认脚本位于仓库的 tools/ 下", file=sys.stderr)
        return 2

    check_frontmatter(root, report)
    files = md_files(root, args.scope)
    check_fences(root, files, report)
    check_links(root, files, report)
    check_whitespace(root, files, report)
    check_vendor(root, report)

    entries, digest = package_manifest(root, pkg_files)
    if args.expect_manifest:
        ok = digest == args.expect_manifest.strip().lower()
        report.add(
            "manifest",
            ok,
            f"包清单 SHA-256 {digest}"
            + ("，与预期一致" if ok else f"，与预期 {args.expect_manifest} 不一致"),
            digest=digest,
            files=len(entries),
        )
    else:
        report.add(
            "manifest",
            True,
            f"包清单 SHA-256 {digest}（{len(entries)} 个文件，未提供预期值，仅记录）",
            digest=digest,
            files=len(entries),
        )

    if args.write_manifest:
        out_path = os.path.join(root, args.write_manifest)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(entries, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"清单已写入 {os.path.relpath(out_path, root)}")

    result = {
        "scope": args.scope,
        "markdown_files_checked": len(files),
        "package_files": len(entries),
        "manifest_sha256": digest,
        "checks": report.checks,
        "failures": report.failures,
        "warnings": report.warnings,
        "ok": not report.failures,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for entry in report.checks:
            if "warning" in entry:
                continue
            print(f"[{'通过' if entry['ok'] else '失败'}] {entry['check']}：{entry['detail']}")
        for warning in report.warnings:
            print(f"[警告] {warning}")
        print(
            f"\n结果：{'全部通过' if not report.failures else str(len(report.failures)) + ' 项失败'}"
            f"（范围 {args.scope}，{len(files)} 个 Markdown 文件，{len(entries)} 个包文件）"
        )
        print("静态检查只证明包材料有效，不代表行为已验证。")
    return 0 if not report.failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
