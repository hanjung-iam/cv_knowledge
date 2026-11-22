"""lint.py — CV Wiki 健康檢查（規格見 CLAUDE.md 第 11 節）。

用法：
    python tools/lint.py                 # 檢查本專案
    python tools/lint.py --root <dir>    # 檢查其他目錄（測試用）
    python tools/lint.py --no-report     # 不寫入 tools/out/lint-report.md

有 error 時 exit code 為 1。
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wikilib as wl  # noqa: E402

COMMON_REQUIRED = ["title", "type", "aliases", "tags", "sources", "related", "created", "updated"]
TYPE_REQUIRED = {
    "source": ["cite_key", "authors", "year", "venue", "raw_path", "url"],
    "model": ["year", "family", "tasks"],
    "task": ["metrics"],
    "concept": [],
    "comparison": [],
    "overview": [],
}
NON_EMPTY = {"title", "type", "created", "updated", "cite_key", "raw_path"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FAMILIES = {"cnn", "transformer", "hybrid"}

# 需要引用的數字：百分比、小數、參數量 / FLOPs、倍數
NUMBER_RE = re.compile(
    r"\d+(?:\.\d+)?\s?%"
    r"|\d+\.\d+"
    r"|\d+(?:\.\d+)?\s?(?:[KMBG]|million|billion)\b"
    r"|\d+(?:\.\d+)?\s?(?:GFLOPs|FLOPs)"
    r"|\d+(?:\.\d+)?\s?(?:×|x)\s?(?:faster|slower|fewer|more|倍)"
    r"|\d+(?:\.\d+)?\s?倍"
)
# source 頁中，「位置」欄這類標記也算引用
LOCATION_RE = re.compile(r"§\s?\d|\bp\.\s?\d|\bTable\s?\d|\bFig\.?\s?\d|\bSec\.?\s?\d")
CONFLICT_OPEN = "⚠️ **來源差異**"
CONFLICT_DONE = "✅ **來源差異（已釐清）**"


class Report:
    def __init__(self):
        self.items: dict[str, list[str]] = {"error": [], "warning": [], "info": []}

    def add(self, level: str, msg: str):
        self.items[level].append(msg)


def check_frontmatter(p: wl.Page, r: Report):
    if p.fm is None:
        r.add("error", f"`{p.rel}`：缺少 frontmatter")
        return
    if p.fm_error:
        r.add("error", f"`{p.rel}`：{p.fm_error}")
    for k in COMMON_REQUIRED:
        if k not in p.fm:
            r.add("error", f"`{p.rel}`：frontmatter 缺少 `{k}`")
    t = p.fm.get("type")
    if t not in wl.PAGE_TYPES:
        r.add("error", f"`{p.rel}`：type `{t}` 不合法（應為 {', '.join(sorted(wl.PAGE_TYPES))}）")
        return
    for k in TYPE_REQUIRED[t]:
        if k not in p.fm:
            r.add("error", f"`{p.rel}`：type={t} 的頁面缺少 `{k}`")
        elif not wl.as_list(p.fm[k]) and k not in NON_EMPTY:
            r.add("warning", f"`{p.rel}`：`{k}` 是空的")
    for k in NON_EMPTY:
        if k in p.fm and not wl.as_list(p.fm[k]):
            r.add("error", f"`{p.rel}`：`{k}` 不可為空")
    for k in ("created", "updated"):
        v = p.fm.get(k)
        if isinstance(v, str) and v and not DATE_RE.match(v):
            r.add("error", f"`{p.rel}`：`{k}` 日期格式應為 YYYY-MM-DD（目前：{v}）")
    if t == "model" and isinstance(p.fm.get("family"), str) and p.fm["family"] not in FAMILIES:
        r.add("error", f"`{p.rel}`：family `{p.fm['family']}` 不合法（應為 {', '.join(sorted(FAMILIES))}）")
    for k in ("sources", "related", "aliases", "tags"):
        if k in p.fm and not isinstance(p.fm[k], list):
            r.add("error", f"`{p.rel}`：`{k}` 應為清單")


def check_links(p: wl.Page, wiki_dir: Path, r: Report):
    for ln, t in p.links:
        if not wl.is_internal(t):
            continue
        if not wl.resolve_link(p, t, wiki_dir).exists():
            r.add("error", f"`{p.rel}:{ln}`：斷掉的連結 `{t}`")
    for rel in wl.as_list((p.fm or {}).get("related")):
        if not (wiki_dir / rel).exists():
            r.add("error", f"`{p.rel}`：frontmatter `related` 中的 `{rel}` 不存在")


def collect_cite_keys(pages: list[wl.Page], r: Report) -> dict[str, str]:
    keys: dict[str, str] = {}
    for p in pages:
        if p.type != "source":
            continue
        k = (p.fm or {}).get("cite_key")
        if not isinstance(k, str) or not k:
            continue
        if not wl.CITE_KEY_RE.match(k):
            r.add("error", f"`{p.rel}`：cite_key `{k}` 格式不合法（只能用英文、數字、連字號，英文開頭）")
        if k in keys:
            r.add("error", f"cite key `{k}` 重複：`{keys[k]}` 與 `{p.rel}`")
        else:
            keys[k] = p.rel
    return keys


def check_citations(p: wl.Page, keys: dict[str, str], r: Report):
    used = set()
    for ln, k, raw in p.cites:
        if k not in keys:
            r.add("error", f"`{p.rel}:{ln}`：引用了不存在的 cite key `{k}`（{raw}）")
        else:
            used.add(k)
    declared = set(wl.as_list((p.fm or {}).get("sources")))
    if p.type == "source" and isinstance((p.fm or {}).get("cite_key"), str):
        used.add(p.fm["cite_key"])  # source 頁本身隱含引用自己
    if p.fm is not None and "sources" in p.fm:
        missing = used - declared
        extra = declared - used
        if missing:
            r.add("warning", f"`{p.rel}`：內文引用了但 `sources` 沒列：{', '.join(sorted(missing))}")
        if extra:
            r.add("warning", f"`{p.rel}`：`sources` 列了但內文沒引用：{', '.join(sorted(extra))}")


def _units(p: wl.Page):
    """把 body 切成檢查單位：表格列、清單項目各自一單位；一般段落為一單位。回傳 (起始行號, 文字)。"""
    buf, start = [], None
    for i, line in p.lines:
        ln = i + p.body_offset
        s = line.strip()
        is_heading = s.startswith("#")
        is_row = s.startswith("|")
        is_item = bool(re.match(r"^(\s*[-*+]|\s*\d+\.)\s", line))
        if not s or is_heading or is_row or is_item:
            if buf:
                yield start, " ".join(buf)
                buf, start = [], None
            if is_row and not re.match(r"^\|[\s:|-]+\|$", s):
                yield ln, s
            elif is_item:
                buf, start = [s], ln   # 清單項目可延續到下一行
            continue
        if start is None:
            start = ln
        buf.append(s)
    if buf:
        yield start, " ".join(buf)


def check_numbers(p: wl.Page, r: Report):
    for ln, text in _units(p):
        has_cite = bool(wl.find_citations(text))
        cleaned = wl.CITE_RE.sub("", wl.LINK_RE.sub("", text))
        nums = NUMBER_RE.findall(cleaned)
        if not nums or has_cite:
            continue
        if p.type == "source" and LOCATION_RE.search(text):
            continue
        sample = ", ".join(dict.fromkeys(n.strip() for n in nums[:3]))
        r.add("warning", f"`{p.rel}:{ln}`：含數字（{sample}）但沒有引用")


def check_index(pages: list[wl.Page], special: dict, wiki_dir: Path, r: Report):
    idx = special.get("index.md")
    if idx is None:
        r.add("error", "缺少 `wiki/index.md`")
        return
    listed = set(wl.internal_page_links(idx, wiki_dir))
    for p in pages:
        if p.rel not in listed:
            r.add("warning", f"`{p.rel}`：沒有列在 index.md")
    check_links(idx, wiki_dir, r)


def check_orphans(pages: list[wl.Page], wiki_dir: Path, r: Report):
    inbound = defaultdict(set)
    for p in pages:
        for dest in wl.internal_page_links(p, wiki_dir):
            if dest != p.rel:
                inbound[dest].add(p.rel)
    for p in pages:
        if p.type == "overview":
            continue
        if not inbound[p.rel]:
            r.add("warning", f"`{p.rel}`：孤兒頁（除了 index 之外沒有頁面連到它）")


def check_raw(root: Path, pages: list[wl.Page], r: Report):
    raw_dir = root / "raw"
    if not raw_dir.exists():
        return
    covered = set()
    for p in pages:
        if p.type == "source":
            for rp in wl.as_list((p.fm or {}).get("raw_path")):
                covered.add(Path(rp).as_posix())
                if not (root / rp).exists():
                    r.add("error", f"`{p.rel}`：raw_path `{rp}` 不存在")
    for f in sorted(raw_dir.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(root).as_posix()
            if rel not in covered:
                r.add("info", f"`{rel}`：尚未 ingest（沒有 source 頁的 raw_path 指向它）")


def check_conflicts(pages: list[wl.Page], r: Report):
    open_n = done_n = 0
    for p in pages:
        for i, line in p.lines:
            if CONFLICT_OPEN in line:
                open_n += 1
                r.add("info", f"`{p.rel}:{i + p.body_offset}`：未釐清的來源差異")
            elif CONFLICT_DONE in line:
                done_n += 1
    r.add("info", f"來源差異統計：未釐清 {open_n}、已釐清 {done_n}")


def run(root: Path) -> tuple[Report, int]:
    wiki_dir, pages, special = wl.load_wiki(root)
    r = Report()
    for p in pages:
        check_frontmatter(p, r)
        check_links(p, wiki_dir, r)
    keys = collect_cite_keys(pages, r)
    for p in pages:
        check_citations(p, keys, r)
        check_numbers(p, r)
    check_index(pages, special, wiki_dir, r)
    check_orphans(pages, wiki_dir, r)
    check_raw(root, pages, r)
    check_conflicts(pages, r)
    return r, len(pages)


def render(r: Report, n_pages: int) -> str:
    e, w, i = (len(r.items[k]) for k in ("error", "warning", "info"))
    out = [f"# Lint Report ({date.today().isoformat()})", "",
           f"頁面數：{n_pages}　|　error：{e}　warning：{w}　info：{i}", ""]
    for level, title in (("error", "Errors"), ("warning", "Warnings"), ("info", "Info")):
        out.append(f"## {title}")
        out.extend(f"- {m}" for m in r.items[level]) if r.items[level] else out.append("（無）")
        out.append("")
    return "\n".join(out)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="CV Wiki lint")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--no-report", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    r, n = run(root)
    text = render(r, n)
    print(text)
    if not args.no_report:
        out = root / "tools" / "out"
        out.mkdir(parents=True, exist_ok=True)
        (out / "lint-report.md").write_text(text, encoding="utf-8")
    sys.exit(1 if r.items["error"] else 0)


if __name__ == "__main__":
    main()
