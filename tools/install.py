#!/usr/bin/env python3
"""把 fucxxx-codex-spec 的四个能力目录安装到 Codex、Claude Code 或 OpenCode。

四个目录总是装进同一个 skills 目录，因此主入口的“并列布局”在安装后同样成立。
只复制四个能力目录；tools、validation、vendor 不随 Skill 安装。

各宿主的发现位置（本机 2026-10-28 核对：codex-cli 0.163.0、Claude Code 2.1.302、
OpenCode 1.19.3）：
    codex     用户级 ${CODEX_HOME:-~/.codex}/skills
    claude    用户级 ~/.claude/skills；项目级 <项目>/.claude/skills
    opencode  用户级 ~/.config/opencode/skills；项目级 <项目>/.opencode/skills
OpenCode 还会自动加载 ~/.claude/skills 与 ~/.agents/skills。已装 claude 用户级时，
再装 opencode 用户级会让 OpenCode 发现两份同名 skill，所以两者不能同时安装。

用法：
    python3 -I tools/install.py --host codex --host claude
    python3 -I tools/install.py --host claude --project /path/to/project
    python3 -I tools/install.py --dest /custom/skills
    python3 -I tools/install.py --host codex --link       # 符号链接到本仓库，便于开发
    python3 -I tools/install.py --host codex --uninstall
    python3 -I tools/install.py --host codex --dry-run

退出码：0 成功（含“已是同版本”）；1 有目标失败或被拒绝；2 用法错误。
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import time

PACKAGES = [
    "fucxxx-codex-spec",
    "fucxxx-codex-spec-init",
    "fucxxx-codex-spec-design",
    "fucxxx-codex-spec-plan",
]


def repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def user_target(host: str) -> str:
    home = os.path.expanduser("~")
    if host == "codex":
        return os.path.join(os.environ.get("CODEX_HOME") or os.path.join(home, ".codex"), "skills")
    if host == "claude":
        return os.path.join(home, ".claude", "skills")
    if host == "opencode":
        return os.path.join(home, ".config", "opencode", "skills")
    raise ValueError(host)


def project_target(host: str, project: str) -> str:
    if host == "claude":
        return os.path.join(project, ".claude", "skills")
    if host == "opencode":
        return os.path.join(project, ".opencode", "skills")
    raise SystemExit(
        "Codex 的项目级 skills 目录没有在本机文档中核实；请改用用户级安装，"
        "或用 --dest 明确指定目录。"
    )


def package_files(base: str) -> dict[str, str]:
    """base 下四个能力目录中全部文件的 {相对路径: SHA-256}，跟随符号链接。"""
    out: dict[str, str] = {}
    for pkg in PACKAGES:
        top = os.path.join(base, pkg)
        if not os.path.exists(top):
            continue
        for dirpath, dirnames, filenames in os.walk(top, followlinks=True):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for name in filenames:
                if name == ".DS_Store":
                    continue
                path = os.path.join(dirpath, name)
                with open(path, "rb") as fh:
                    out[os.path.relpath(path, base)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def manifest_digest(entries: dict[str, str]) -> str:
    """与 tools/check-package.py 相同的包清单算法。"""
    blob = "".join(f"{rel}\t{h}\n" for rel, h in sorted(entries.items()))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def skill_name(skill_dir: str) -> str | None:
    """读取 SKILL.md frontmatter 的 name；读不到返回 None。"""
    path = os.path.join(skill_dir, "SKILL.md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    for line in text[3:].split("\n---", 1)[0].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def ours(path: str, pkg: str) -> bool:
    """目标位置的同名目录是否就是本包的这个能力。"""
    return os.path.isdir(path) and skill_name(path) == pkg


def backup_root(dest: str) -> str:
    """备份放在 skills 目录之外：OpenCode 会递归扫描 **/SKILL.md，放在里面会被当成 skill。"""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return os.path.join(os.path.dirname(os.path.abspath(dest)), "fucxxx-codex-spec-backups", stamp)


def install(src_root: str, dest: str, link: bool, force: bool, dry: bool) -> bool:
    src_entries = package_files(src_root)
    src_digest = manifest_digest(src_entries)
    print(f"\n目标：{dest}")

    existing = {pkg: os.path.join(dest, pkg) for pkg in PACKAGES if os.path.lexists(os.path.join(dest, pkg))}
    for pkg, path in existing.items():
        if not os.path.islink(path) and not ours(path, pkg):
            print(f"  拒绝：{path} 已存在且不是本包的 {pkg}（SKILL.md 的 name 不符），不会覆盖。")
            return False

    if existing:
        current = package_files(dest)
        if len(existing) == len(PACKAGES) and manifest_digest(current) == src_digest:
            mode = "符号链接" if all(os.path.islink(p) for p in existing.values()) else "副本"
            want = "符号链接" if link else "副本"
            if mode == want:
                print(f"  已是同版本（{src_digest[:12]}，{mode}），无需改动。")
                report_registration(dest)
                return True
        if not force:
            print(f"  目标已有本包的其他版本或不完整安装：{', '.join(existing)}。")
            print("  加 --force 替换；旧版会先备份到 skills 目录之外。")
            return False

    if dry:
        verb = "链接" if link else "复制"
        print(f"  [dry-run] 将{verb} {len(PACKAGES)} 个目录（{len(src_entries)} 个文件，包清单 {src_digest[:12]}）。")
        if existing:
            print(f"  [dry-run] 将先备份并替换：{', '.join(existing)} -> {backup_root(dest)}")
        return True

    os.makedirs(dest, exist_ok=True)
    if existing:
        bk = backup_root(dest)
        os.makedirs(bk, exist_ok=True)
        for pkg, path in existing.items():
            if os.path.islink(path):
                os.unlink(path)
            else:
                shutil.move(path, os.path.join(bk, pkg))
        print(f"  旧版已移到：{bk}")

    for pkg in PACKAGES:
        src = os.path.join(src_root, pkg)
        dst = os.path.join(dest, pkg)
        if link:
            os.symlink(src, dst)
        else:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store"))

    got = manifest_digest(package_files(dest))
    if got != src_digest:
        print(f"  失败：安装后包清单 {got[:12]} 与源 {src_digest[:12]} 不一致。")
        return False
    print(f"  已{'链接' if link else '复制'} {len(PACKAGES)} 个目录，包清单 {got} 与源一致。")
    report_registration(dest)
    return True


def uninstall(dest: str, dry: bool) -> bool:
    print(f"\n目标：{dest}")
    ok = True
    removed = 0
    for pkg in PACKAGES:
        path = os.path.join(dest, pkg)
        if not os.path.lexists(path):
            continue
        if not os.path.islink(path) and not ours(path, pkg):
            print(f"  跳过：{path} 不是本包的 {pkg}，不删除。")
            ok = False
            continue
        if dry:
            print(f"  [dry-run] 将移除 {path}")
        elif os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)
        removed += 1
    print(f"  {'将移除' if dry else '已移除'} {removed} 个目录。" if removed else "  没有可移除的本包目录。")
    return ok


def report_registration(dest: str) -> None:
    """接入时写进项目 AGENTS.md 的登记值（见 init 能力的接入片段）。"""
    print("  AGENTS.md 登记值：")
    print(f"    Skill 入口：{os.path.join(dest, PACKAGES[0], 'SKILL.md')}")
    print(f"    Skill 包根：{dest}")
    print("    阶段能力入口：同包根")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="安装 fucxxx-codex-spec 的四个能力目录")
    ap.add_argument("--host", action="append", choices=["codex", "claude", "opencode"], default=[],
                    help="目标宿主，可重复；用户级位置见文件头说明")
    ap.add_argument("--project", metavar="DIR", help="改为安装到该项目的项目级目录（claude、opencode）")
    ap.add_argument("--dest", metavar="DIR", help="直接指定 skills 目录，忽略 --host")
    ap.add_argument("--link", action="store_true", help="符号链接到本仓库而非复制（开发用，随仓库改动即时生效）")
    ap.add_argument("--force", action="store_true", help="替换已安装的其他版本，旧版先备份")
    ap.add_argument("--uninstall", action="store_true", help="移除已安装的四个目录（只删本包的目录）")
    ap.add_argument("--dry-run", action="store_true", help="只显示将做什么")
    args = ap.parse_args(argv)

    if args.dest:
        targets = [os.path.abspath(os.path.expanduser(args.dest))]
    elif args.host:
        hosts = list(dict.fromkeys(args.host))
        if not args.project and "claude" in hosts and "opencode" in hosts:
            print("claude 与 opencode 不能同时做用户级安装：OpenCode 会自动加载 ~/.claude/skills，"
                  "两处都装会出现同名 skill。只装 claude 即可同时供 Claude Code 与 OpenCode 使用。",
                  file=sys.stderr)
            return 2
        targets = [project_target(h, os.path.abspath(args.project)) if args.project else user_target(h)
                   for h in hosts]
    else:
        ap.error("需要 --host 或 --dest")

    src = repo_root()
    if len(package_files(src)) == 0:
        print("未在脚本所在仓库找到能力目录。", file=sys.stderr)
        return 2

    results = [uninstall(t, args.dry_run) if args.uninstall else install(src, t, args.link, args.force, args.dry_run)
               for t in targets]
    if not args.uninstall and not args.dry_run and all(results):
        print("\n新会话才会发现新装的 skill；已打开的会话需要重启。")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
