#!/usr/bin/env python3
"""
Nanobanana (Gemini Image Generation) API を使って画像を生成し output/images/ に保存する。

使い方:
  python generate.py --prompt "プロンプトテキスト" --output "ファイル名.png"
  python generate.py --from-report   # shared/04_image_report.md からプロンプトを読み込む
"""

import argparse
import base64
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.getenv("GOOGLE_AI_API_KEY")
if not API_KEY:
    print("エラー: .env に GOOGLE_AI_API_KEY が設定されていません", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent.parent / "output" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = Path(__file__).parent.parent / "shared" / "04_image_report.md"

MODEL = "gemini-2.0-flash-preview-image-generation"


def generate_image(prompt: str, output_filename: str) -> Path:
    client = genai.Client(api_key=API_KEY)

    print(f"画像生成中: {output_filename}")
    print(f"プロンプト: {prompt[:80]}...")

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"]
        ),
    )

    output_path = OUTPUT_DIR / output_filename
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = base64.b64decode(part.inline_data.data)
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"保存完了: {output_path}")
            return output_path

    raise RuntimeError("画像データが返されませんでした。プロンプトを確認してください。")


def extract_prompts_from_report(report_path: Path) -> list[dict]:
    """shared/04_image_report.md から [IMAGE_PROMPT] ブロックを抽出する。"""
    text = report_path.read_text(encoding="utf-8")
    blocks = re.findall(
        r"###\s*(.+?)\n```\n\[IMAGE_PROMPT\]\n(.*?)```",
        text,
        re.DOTALL,
    )
    prompts = []
    for title, prompt_body in blocks:
        prompts.append({
            "title": title.strip(),
            "prompt": prompt_body.strip(),
        })
    return prompts


def update_report(report_path: Path, title: str, saved_path: Path):
    """生成済みファイルパスをレポートの管理表に記録する。"""
    text = report_path.read_text(encoding="utf-8")
    row = f"| - | {title} | {saved_path.name} | 生成済み |\n"
    text = text.replace("| 1 | アイキャッチ | | 未生成 |\n", row, 1)
    report_path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Nanobanana 画像生成スクリプト")
    parser.add_argument("--prompt", type=str, help="画像生成プロンプト")
    parser.add_argument("--output", type=str, help="出力ファイル名（例: eyecatch_01.png）")
    parser.add_argument(
        "--from-report",
        action="store_true",
        help="shared/04_image_report.md からプロンプトを読み込む",
    )
    args = parser.parse_args()

    if args.from_report:
        if not REPORT_PATH.exists():
            print(f"エラー: {REPORT_PATH} が見つかりません", file=sys.stderr)
            sys.exit(1)
        prompts = extract_prompts_from_report(REPORT_PATH)
        if not prompts:
            print("レポートに [IMAGE_PROMPT] ブロックが見つかりませんでした。", file=sys.stderr)
            sys.exit(1)
        for i, item in enumerate(prompts, 1):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{i:02d}_{timestamp}.png"
            saved = generate_image(item["prompt"], filename)
            update_report(REPORT_PATH, item["title"], saved)
    elif args.prompt and args.output:
        generate_image(args.prompt, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
