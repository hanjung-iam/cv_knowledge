"""review.py — 全域 lint（schema 9.3）的人工審查輔助報告。

lint.py 檢查「格式對不對」；review.py 不判斷對錯，而是把需要人工判斷的線索整理出來：

1. 跨頁數字：同一個數字出現在哪些頁面（檢查寫法和條件是否一致）
2. 未連結的提及：A 頁提到 B 頁的標題或別名，卻沒有連到 B 頁
3. 候選新頁面：在多個頁面被粗體強調、卻沒有自己頁面的術語
4. 數學符號：各頁使用的希臘字母符號（找出同一概念用了不同符號的地方）
5. 待重新檢視的段落：（綜合推論）與「待補／下一步」等前瞻性用語，新來源加入後可能已過時

用法：
    python tools/review.py                # 輸出到終端機與 tools/out/review-report.md
    python tools/review.py --root <dir>   # 測試用
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

BS = chr(92)  # 反斜線，避免在 regex 字串中跳脫出錯
NUMBER_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+\.\d+%?|\d+%)(?![\w.])")
BOLD_RE = re.compile(r"\*\*([^*\n]{2,40})\*\*")
GREEK = ["alpha", "beta", "gamma", "delta", "Delta", "epsilon", "lambda", "mu", "sigma", "theta", "eta"]
FORWARD_RE = re.compile(r"待補|下一步|下一站|之後的來源|目前收錄的來源沒有|尚未")
MIN_PAGES_NUMBER = 2
MIN_PAGES_BOLD = 3


def body_text(p: wl.Page) -> str:
    return "\n".join(line for _, line in p.lines)


def section_numbers(pages):
    where = defaultdict(set)
    for p in pages:
        if p.type == "source":
            continue  # source 頁本來就會重複列出數字，不列入
        for n in NUMBER_RE.findall(body_text(p)):
            where[n].add(p.rel)
    rows = sorted(((n, sorted(ps)) for n, ps in where.items() if len(ps) >= MIN_PAGES_NUMBER),
                  key=lambda x: (-len(x[1]), x[0]))
    out = ["## 1. 跨頁數字（出現在 ≥2 個非 source 頁面）", "",
           "逐一確認：各頁的數字是否相同、條件（資料集、設定）是否寫清楚。", ""]
    out += [f"- `{n}`：{', '.join(ps)}" for n, ps in rows] or ["（無）"]
    return out


def section_unlinked(pages, wiki_dir):
    names = {}
    for p in pages:
        if p.type == "source":
            continue
        cands = [p.title] + [a for a in wl.as_list((p.fm or {}).get("aliases")) if re.search(r"[A-Za-z]", a)]
        for c in cands:
            c = re.sub(r"（.*?）|\(.*?\)", "", c).strip()
            if len(c) >= 4:
                names[c] = p.rel
    out = ["## 2. 未連結的提及", "",
           "A 頁提到了 B 頁的標題或英文別名，但全頁都沒有連到 B 頁。不一定要修，請判斷是否該加連結。", ""]
    found = []
    for p in pages:
        linked = set(wl.internal_page_links(p, wiki_dir))
        # 先移除連結和引用標記：引用裡的檔名或小節標題（例如 optimization-1、"Nearest Neighbor Classifier"）不算提及
        text = wl.CITE_RE.sub("", wl.LINK_RE.sub("", body_text(p)))
        missing = defaultdict(list)
        for name, dest in names.items():
            if dest == p.rel or dest in linked:
                continue
            # 後面接連字號的不算（例如「optimization-1 筆記」是檔名，不是 Optimization 概念）
            if re.search(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z-])", text, re.I):
                missing[dest].append(name)
        for dest, ns in sorted(missing.items()):
            found.append(f"- `{p.rel}` 提到 {', '.join(sorted(set(ns)))}，但沒有連到 `{dest}`")
    return out + (found or ["（無）"])


def section_candidates(pages):
    known = set()
    for p in pages:
        known.add(p.title.lower())
        known.update(a.lower() for a in wl.as_list((p.fm or {}).get("aliases")))
    where = defaultdict(set)
    for p in pages:
        if p.type == "source":
            continue
        for term in BOLD_RE.findall(body_text(p)):
            t = term.strip()
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9 \-]+", t) and t.lower() not in known:
                where[t.lower()].add(p.rel)
    rows = sorted(((t, sorted(ps)) for t, ps in where.items() if len(ps) >= MIN_PAGES_BOLD),
                  key=lambda x: -len(x[1]))
    out = ["## 3. 候選新頁面", "",
           f"在 ≥{MIN_PAGES_BOLD} 個頁面被粗體強調、但不是任何頁面標題或別名的英文術語。"
           "是否建頁仍要看來源是否有足夠內容。", ""]
    return out + ([f"- **{t}**（{len(ps)} 頁）：{', '.join(ps)}" for t, ps in rows] or ["（無）"])


def section_symbols(pages):
    out = ["## 4. 數學符號", "", "各頁使用的希臘字母。同一概念在不同頁面用了不同符號時要統一（或註明）。", ""]
    rows = []
    for g in GREEK:
        pat = re.compile(re.escape(BS + g) + r"(?![A-Za-z])")
        hits = [(p.rel, len(pat.findall(body_text(p)))) for p in pages]
        hits = [(r, c) for r, c in hits if c]
        if hits:
            rows.append(f"- `{BS}{g}`：" + ", ".join(f"{r}({c})" for r, c in hits))
    return out + (rows or ["（無）"])


def section_revisit(pages):
    out = ["## 5. 待重新檢視的段落", "",
           "（綜合推論）和前瞻性用語，在新來源加入後可能已經過時或被修正。", ""]
    rows = []
    for p in pages:
        if p.type == "source":
            continue
        for i, line in p.lines:
            ln = i + p.body_offset
            s = line.strip()
            if "綜合推論" in s:
                rows.append(f"- `{p.rel}:{ln}`（綜合推論）：{s[:80]}…")
            elif FORWARD_RE.search(s):
                rows.append(f"- `{p.rel}:{ln}`（前瞻性用語）：{s[:80]}…")
    return out + (rows or ["（無）"])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="CV Wiki global review helper")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--no-report", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    wiki_dir, pages, _ = wl.load_wiki(root)
    lines = [f"# Global Review Report ({date.today().isoformat()})", "", f"頁面數：{len(pages)}", ""]
    for sec in (section_numbers(pages), section_unlinked(pages, wiki_dir), section_candidates(pages),
                section_symbols(pages), section_revisit(pages)):
        lines += sec + [""]
    text = "\n".join(lines)
    print(text)
    if not args.no_report:
        out = root / "tools" / "out"
        out.mkdir(parents=True, exist_ok=True)
        (out / "review-report.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
