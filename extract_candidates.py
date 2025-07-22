#!/usr/bin/env python3
import fitz  # PyMuPDF
import csv
import os
import re
from collections import Counter

INPUT_DIR = "dataset"
OUTPUT_CSV = "candidates.csv"

# a small set of common math symbols
MATH_SYMBOLS = set("=+−-*/^()[]{}<>×÷∑∏√∞π")

def normalize_text(text: str) -> str:
    """
    Merge stray single-letter tokens into their following token,
    e.g. ["I","NTRODUCTION"] -> ["INTRODUCTION"].
    """
    tokens = text.split()
    merged = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if len(tok) == 1 and tok.isupper() and (i + 1) < len(tokens):
            nxt = tokens[i + 1]
            if nxt.isupper():
                merged.append(tok + nxt)
                i += 2
                continue
        merged.append(tok)
        i += 1
    return " ".join(merged)

def extract_blocks(pdf_path):
    """Extract merged text blocks from a PDF, preserving font info."""
    doc = fitz.open(pdf_path)
    raw = []
    font_sizes = []

    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                spans = sorted(line["spans"], key=lambda s: s["origin"][0])
                if not spans:
                    continue

                first = spans[0]
                fs = first["size"]
                fname = first["font"]
                is_bold = bool(re.search(r"bold|black", fname, re.IGNORECASE))
                x0, y0 = first["origin"]

                # merge spans
                text = ""
                for sp in spans:
                    chunk = sp["text"].strip()
                    if not chunk:
                        continue
                    if text and not re.match(r"[,\.\)\]]", chunk):
                        text += " "
                    text += chunk
                text = text.strip()
                if not text:
                    continue

                text = normalize_text(text)

                raw.append({
                    "text": text,
                    "page": page.number + 1,
                    "font_size": fs,
                    "is_bold": int(is_bold),
                    "x": int(x0),
                    "y": int(y0),
                    "char_length": len(text),
                })
                font_sizes.append(fs)

    doc.close()
    body_font = Counter(font_sizes).most_common(1)[0][0] if font_sizes else None
    return raw, body_font

def is_numerically_dense(text: str, threshold: float = 0.2) -> bool:
    """Return True if digits+math symbols exceed threshold proportion."""
    length = len(text)
    if length == 0:
        return True
    count = sum(ch.isdigit() or ch in MATH_SYMBOLS for ch in text)
    return (count / length) >= threshold

def main():
    rows = []
    for fname in sorted(os.listdir(INPUT_DIR)):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(INPUT_DIR, fname)
        print(f"→ scanning {fname}")
        blocks, body_font = extract_blocks(path)

        for b in blocks:
            fs = b["font_size"]
            bold = b["is_bold"]
            length = b["char_length"]
            txt = b["text"]

            # 1) font-size filter
            if body_font is None:
                continue
            if fs < body_font:
                continue
            if fs == body_font and not bold:
                continue

            # 2) length filter
            if length <= 3 or length >= 100:
                continue

            # 3) numeric/formula density filter
            if is_numerically_dense(txt):
                continue

            rows.append({
                "document": fname,
                "page": b["page"],
                "text": txt,
                "font_size": fs,
                "is_bold": bold,
                "x": b["x"],
                "y": b["y"],
                "char_length": length,
                "body_font_size": body_font,
                "heading": 0
            })

    # with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    # use 'utf-8-sig' so tools like Excel pick up UTF‑8 properly
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "document","page","text","font_size","is_bold",
            "x","y","char_length","body_font_size","heading"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"✅ Wrote {len(rows)} candidates to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
