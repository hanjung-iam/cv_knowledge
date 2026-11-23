"""pdf_tools.py — ingest 時讀取 PDF 的輔助工具（需要 cv_wiki_env 虛擬環境中的 PyMuPDF）。

用法（在專案根目錄執行）：
    cv_wiki_env/Scripts/python tools/pdf_tools.py info   <pdf>
    cv_wiki_env/Scripts/python tools/pdf_tools.py text   <pdf> <out.txt>
    cv_wiki_env/Scripts/python tools/pdf_tools.py render <pdf> <out_dir> <pages> [dpi]
    cv_wiki_env/Scripts/python tools/pdf_tools.py images <pdf> <out_dir>

- info：顯示 producer、頁數、每頁文字字元數、字型數、向量繪圖數、內嵌圖片數，
        並判斷文字是否可抽取（「Microsoft: Print To PDF」常把文字轉成向量外框，無法抽取）。
- text：抽出全文，每頁前面加上 `=== page N ===`。
- render：把指定頁面畫成 PNG（pages 例如 `1,3-5`），可以看到向量圖（例如論文的架構圖、訓練曲線）。
- images：抽出內嵌的點陣圖片。

輸出請放在專案外的暫存目錄，不要放進 wiki/ 或 raw/。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:  # pragma: no cover
    sys.exit("需要 PyMuPDF：請用 cv_wiki_env/Scripts/python 執行（見 requirements.txt）")


def parse_pages(spec: str) -> list[int]:
    pages: list[int] = []
    for part in spec.split(","):
        a, _, b = part.strip().partition("-")
        pages += range(int(a), int(b or a) + 1)
    return pages


def cmd_info(pdf: str):
    d = pymupdf.open(pdf)
    meta = {k: v for k, v in d.metadata.items() if v and k in ("title", "author", "producer", "creator")}
    print(f"檔案：{pdf}")
    print(f"頁數：{d.page_count}　metadata：{meta}")
    total = 0
    for i, p in enumerate(d, 1):
        n = len(p.get_text())
        total += n
        print(f"  p{i:02d}  text={n:6d}  fonts={len(p.get_fonts()):2d}  "
              f"drawings={len(p.get_drawings()):5d}  images={len(p.get_images()):2d}")
    print(f"文字字元總數：{total}")
    if total == 0:
        print("⚠ 抽不出文字：文字可能被轉成向量外框（常見於 Microsoft Print To PDF）。"
              "請改用 render 看頁面，或改用瀏覽器內建的「另存為 PDF」重新存檔。")


def cmd_text(pdf: str, out: str):
    d = pymupdf.open(pdf)
    text = "\n\n".join(f"=== page {i} ===\n{p.get_text()}" for i, p in enumerate(d, 1))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(text, encoding="utf-8")
    print(f"{out}（{len(text)} 字元）")


def cmd_render(pdf: str, out_dir: str, spec: str, dpi: int = 110):
    d = pymupdf.open(pdf)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for n in parse_pages(spec):
        f = out / f"p{n:02d}.png"
        d[n - 1].get_pixmap(dpi=dpi).save(f)
        print(f)


def cmd_images(pdf: str, out_dir: str):
    d = pymupdf.open(pdf)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    k = 0
    for i, p in enumerate(d, 1):
        for xref, *_ in p.get_images(full=True):
            info = d.extract_image(xref)
            k += 1
            f = out / f"p{i:02d}_{k:02d}.{info['ext']}"
            f.write_bytes(info["image"])
            print(f, info["width"], "x", info["height"])
    if k == 0:
        print("沒有內嵌的點陣圖片（圖可能是向量圖，請改用 render）。")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "info":
        cmd_info(*args[:1])
    elif cmd == "text":
        cmd_text(*args[:2])
    elif cmd == "render":
        cmd_render(args[0], args[1], args[2], int(args[3]) if len(args) > 3 else 110)
    elif cmd == "images":
        cmd_images(*args[:2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
