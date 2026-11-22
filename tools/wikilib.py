"""wikilib — lint.py 與 graph.py 共用的 Wiki 解析函式（只用標準函式庫）。

Wiki 規範見 CLAUDE.md。這裡只負責「讀」：frontmatter、連結、引用。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# 不視為一般 Wiki 頁面的特殊檔案（相對於 wiki/）
SPECIAL_PAGES = {"index.md", "log.md"}

PAGE_TYPES = {"model", "task", "concept", "source", "comparison", "overview"}

# ---------------------------------------------------------------- frontmatter

def _strip_comment(s: str) -> str:
    """去掉行尾的 `  # 註解`（不在引號內、且 # 前面有空白）。"""
    in_q = None
    for i, ch in enumerate(s):
        if ch in "\"'":
            if in_q is None:
                in_q = ch
            elif in_q == ch:
                in_q = None
        elif ch == "#" and in_q is None and (i == 0 or s[i - 1].isspace()):
            return s[:i].rstrip()
    return s.rstrip()


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _parse_inline_list(s: str) -> list[str]:
    inner = s.strip()[1:-1]
    items, buf, in_q = [], "", None
    for ch in inner:
        if ch in "\"'":
            in_q = None if in_q == ch else (ch if in_q is None else in_q)
            buf += ch
        elif ch == "," and in_q is None:
            items.append(buf)
            buf = ""
        else:
            buf += ch
    items.append(buf)
    return [_unquote(x) for x in items if x.strip()]


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None, int]:
    """回傳 (frontmatter dict 或 None, body, 錯誤訊息或 None, body 起始行號)。

    只支援本 Wiki 用到的 YAML 子集：
      key: value / key: "value" / key: [a, b] / key: 後接多行 `- item`
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text, None, 1
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text, "frontmatter 沒有結尾的 `---`", 1

    data: dict = {}
    current_list_key = None
    for ln_no, raw in enumerate(lines[1:end], start=2):
        line = _strip_comment(raw)
        if not line.strip():
            continue
        m_item = re.match(r"^\s+-\s*(.*)$", line)
        if m_item:
            if current_list_key is None:
                return data, "\n".join(lines[end + 1:]), f"frontmatter 第 {ln_no} 行：清單項目沒有對應的 key", end + 2
            data[current_list_key].append(_unquote(m_item.group(1)))
            continue
        m_kv = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m_kv:
            return data, "\n".join(lines[end + 1:]), f"frontmatter 第 {ln_no} 行無法解析：{raw.strip()}", end + 2
        key, val = m_kv.group(1), m_kv.group(2).strip()
        if val == "":
            data[key] = []
            current_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            data[key] = _parse_inline_list(val)
            current_list_key = None
        else:
            data[key] = _unquote(val)
            current_list_key = None
    return data, "\n".join(lines[end + 1:]), None, end + 2


def as_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v] if str(v).strip() else []

# ---------------------------------------------------------------- body 解析

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^()\s]+)(?:\s+\"[^\"]*\")?\)")
IMG_RE = re.compile(r"!\[([^\[\]]*)\]\(([^()\s]+)\)")
# 引用：[KEY ...] 或 [KEY ...; KEY2 ...]，後面不能接 `(`（那是連結）
CITE_RE = re.compile(r"\[([^\[\]\n]+)\](?!\()")
CITE_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9\-]*$")


def strip_code(body: str) -> list[tuple[int, str]]:
    """回傳 [(行號(相對 body, 從 0 起), 行內容)]；fenced code 內的行以空字串取代，inline code 移除。"""
    out = []
    in_fence = False
    for i, line in enumerate(body.split("\n")):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append((i, ""))
            continue
        out.append((i, "" if in_fence else INLINE_CODE_RE.sub("", line)))
    return out


def find_links(line: str) -> list[str]:
    targets = [m.group(2) for m in LINK_RE.finditer(line)]
    targets += [m.group(2) for m in IMG_RE.finditer(line)]
    return targets


def is_internal(target: str) -> bool:
    return not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) and not target.startswith("#")


def find_citations(line: str) -> list[tuple[str, str]]:
    """回傳 [(key, 完整引用文字)]。只把「第一個 token 像 cite key」的方括號視為引用。"""
    line = LINK_RE.sub("", line)
    out = []
    for m in CITE_RE.finditer(line):
        content = m.group(1).strip()
        parts = [p.strip() for p in content.split(";") if p.strip()]
        keys = []
        for p in parts:
            first = p.split()[0]
            if not CITE_KEY_RE.match(first):
                keys = []
                break
            keys.append(first)
        # 純英文單字、且整段只有一個 token 的方括號（例如 [x]、[TODO]）也算引用，交給 lint 判斷 key 是否存在
        for k in keys:
            out.append((k, m.group(0)))
    return out

# ---------------------------------------------------------------- 頁面

@dataclass
class Page:
    path: Path               # 絕對路徑
    rel: str                 # 相對於 wiki/ 的 posix 路徑
    fm: dict | None
    fm_error: str | None
    body: str
    body_offset: int         # body 第一行在檔案中的行號（1 起）
    lines: list[tuple[int, str]] = field(default_factory=list)  # strip_code 後
    links: list[tuple[int, str]] = field(default_factory=list)  # (檔案行號, target)
    cites: list[tuple[int, str, str]] = field(default_factory=list)  # (檔案行號, key, 原文)

    @property
    def type(self) -> str:
        return (self.fm or {}).get("type", "") if isinstance((self.fm or {}).get("type", ""), str) else ""

    @property
    def title(self) -> str:
        t = (self.fm or {}).get("title")
        return t if isinstance(t, str) and t else self.path.stem


def load_page(path: Path, wiki_dir: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    fm, body, err, offset = parse_frontmatter(text)
    p = Page(path=path, rel=path.relative_to(wiki_dir).as_posix(), fm=fm, fm_error=err,
             body=body, body_offset=offset)
    p.lines = strip_code(body)
    for i, line in p.lines:
        ln = i + offset
        for t in find_links(line):
            p.links.append((ln, t))
        for k, raw in find_citations(line):
            p.cites.append((ln, k, raw))
    return p


def load_wiki(root: Path) -> tuple[Path, list[Page], dict[str, Page]]:
    """回傳 (wiki_dir, 一般頁面清單, 特殊頁面 dict)。"""
    wiki_dir = root / "wiki"
    pages, special = [], {}
    for f in sorted(wiki_dir.rglob("*.md")):
        p = load_page(f, wiki_dir)
        if p.rel in SPECIAL_PAGES:
            special[p.rel] = p
        else:
            pages.append(p)
    return wiki_dir, pages, special


def resolve_link(page: Page, target: str, wiki_dir: Path) -> Path:
    target = target.split("#", 1)[0]
    from urllib.parse import unquote
    return (page.path.parent / unquote(target)).resolve()


def internal_page_links(page: Page, wiki_dir: Path) -> list[str]:
    """回傳本頁連到的 Wiki 頁面（相對於 wiki/ 的路徑，去重、保序）。"""
    seen, out = set(), []
    wiki_res = wiki_dir.resolve()
    for _, t in page.links:
        if not is_internal(t) or not t.split("#", 1)[0].endswith(".md"):
            continue
        dest = resolve_link(page, t, wiki_dir)
        try:
            rel = dest.relative_to(wiki_res).as_posix()
        except ValueError:
            continue
        if dest.exists() and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out
