#!/usr/bin/env python3
import os
import json
from extract_candidates import extract_blocks, normalize_text
from utils import HeadingDetector
from collections import Counter

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def determine_heading_level(font_size: float, body_font: float) -> str:
    if body_font is None:
        return "H3"
    ratio = font_size / body_font
    if ratio >= 1.5:
        return "H1"
    elif ratio >= 1.2:
        return "H2"
    else:
        return "H3"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    detector = HeadingDetector(model_path="model/heading_model.pkl")

    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(INPUT_DIR, filename)
        print(f"Processing {filename}")
        blocks, body_font, _ = extract_blocks(pdf_path)

        outline = []
        title = None

        for b in blocks:
            if len(b["text"]) < 3 or len(b["text"]) > 100:
                continue

            # Calculate font_ratio
            font_ratio = b["font_size"] / body_font if body_font else 1.0

            features = {
                "font_size": b["font_size"],
                "is_bold": b["is_bold"],
                "x": b["x"],
                "y": b["y"],
                "char_length": b["char_length"],
                "body_font_size": body_font,
                "font_ratio": font_ratio,
                "text": b["text"]
            }

            if detector.is_heading(features):
                level = determine_heading_level(b["font_size"], body_font)

                if title is None or level == "H1":
                    title = b["text"]

                outline.append({
                    "level": level,
                    "text": b["text"],
                    "page": b["page"]
                })

        # Fallback title
        if not title:
            title = "Untitled Document"

        result = {
            "title": title,
            "outline": outline
        }

        # Save output JSON
        base = os.path.splitext(filename)[0]
        out_path = os.path.join(OUTPUT_DIR, f"{base}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved output to {out_path}")

if __name__ == "__main__":
    main()
