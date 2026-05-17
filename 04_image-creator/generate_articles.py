"""
各記事のアイキャッチ画像を一括生成するスクリプト。
実行前に ../.env に GOOGLE_AI_API_KEY を設定してください。

使い方:
  cd 04_image-creator
  python3 generate_articles.py
"""

import sys
from generate import generate_image

ARTICLES = [
    {
        "id": "00",
        "title": "自己紹介",
        "filename": "00_self-introduction.png",
        "concept": "C. ストリートカルチャー型",
        "prompt": (
            "Cardboard boxes filled with folded streetwear t-shirts stacked in a dim storage room, "
            "representing unsold inventory from a first apparel business attempt, "
            "urban warehouse aesthetic with exposed brick walls and warm tungsten lighting, "
            "moody cinematic atmosphere, shallow depth of field with bokeh background, "
            "high-resolution commercial photography, sharp focus on the foreground boxes, "
            "16:9 aspect ratio, no text overlay, no watermark, no people's faces, no brand logos"
        ),
    },
    {
        "id": "01",
        "title": "全体マップ",
        "filename": "01_overall-map.png",
        "concept": "B. 作業・工程フォーカス型",
        "prompt": (
            "Overhead flat lay photography on dark concrete surface: fabric swatches in streetwear earth tones, "
            "open notebook with brand design sketches and directional arrows, laptop computer, DSLR camera, "
            "smartphone showing a clean Instagram grid, measuring tape, and pen, "
            "arranged in a circular flow composition suggesting a five-step process, "
            "urban creative workspace aesthetic, dramatic side lighting with warm amber tones, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "02",
        "title": "アパレルの作り方3選",
        "filename": "02_manufacturing-methods.png",
        "concept": "B. 作業・工程フォーカス型",
        "prompt": (
            "Three distinct apparel production routes displayed as a flat-lay concept on dark concrete surface: "
            "left section shows neatly folded streetwear t-shirts on a domestic printing bed, "
            "center section shows fabric swatches and samples representing China OEM manufacturing, "
            "right section shows packaged clothing items sealed in clear poly bags representing drop-shipping, "
            "dramatic industrial lighting with warm amber and cool blue tones, "
            "urban warehouse aesthetic, street fashion mood, "
            "high-resolution commercial photography, sharp focus, 16:9 aspect ratio, "
            "no text overlay, no watermark, no people's faces, no brand logos"
        ),
    },
    {
        "id": "03",
        "title": "印刷の種類6選",
        "filename": "03_printing-guide.png",
        "concept": "B. 作業・工程フォーカス型",
        "prompt": (
            "Close-up detail of a professional screen printing press with ink-filled squeegee and vibrant colored inks, "
            "alongside fabric swatches showing different printing textures — bold graphic print, embroidery, "
            "heat transfer film — arranged on a dark workshop table, "
            "industrial workshop aesthetic, dramatic raking side light emphasizing texture, "
            "high-resolution commercial photography, sharp focus on print details, "
            "16:9 aspect ratio, no text overlay, no watermark, no people's faces, no brand logos"
        ),
    },
    {
        "id": "04",
        "title": "コスト全公開",
        "filename": "04_cost-breakdown.png",
        "concept": "D. インフォグラフィック型",
        "prompt": (
            "Overhead flat lay on dark slate surface: a stack of fabric swatches, a simple calculator, "
            "an open notebook with handwritten cost breakdown columns, "
            "neatly arranged shipping labels, small coin pile, and a pen, "
            "suggesting apparel business cost analysis, "
            "clean urban workspace aesthetic, soft directional lighting, minimal composition, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "05",
        "title": "入稿データの作り方",
        "filename": "05_submission-data.png",
        "concept": "B. 作業・工程フォーカス型",
        "prompt": (
            "Close-up of a laptop screen displaying vector graphic design software with a streetwear t-shirt graphic, "
            "beside a printed color swatch guide, a USB drive, and a ruler on a dark desk, "
            "suggesting digital print file preparation, creative workspace aesthetic, "
            "blue-toned monitor glow against dark background, cinematic lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "06",
        "title": "パッケージ・タグ",
        "filename": "06_packaging-tags.png",
        "concept": "A. 商品・素材フォーカス型",
        "prompt": (
            "Elegant flat lay of streetwear brand packaging elements on dark concrete: "
            "woven clothing label, printed hang tag, clear OPP poly bag, small kraft paper shopping bag, "
            "and a folded black t-shirt, "
            "arranged with intentional spacing, warm spotlight lighting highlighting fabric textures, "
            "luxury minimalist aesthetic, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "07",
        "title": "ブランド名・商標登録",
        "filename": "07_brand-name-trademark.png",
        "concept": "D. インフォグラフィック型",
        "prompt": (
            "Overhead flat lay on dark wood surface: open notebook with hand-lettered brand name concepts and circles, "
            "an official-looking document stamp, a fountain pen, and a small woven clothing label, "
            "suggesting brand naming and trademark registration process, "
            "clean and authoritative aesthetic, soft diffused lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "08",
        "title": "ブランドコンセプト",
        "filename": "08_brand-concept.png",
        "concept": "C. ストリートカルチャー型",
        "prompt": (
            "Urban mood board flat lay on dark concrete: torn magazine cutouts in street style aesthetic, "
            "paint swatches in earth and monochrome tones, polaroid-style photos of urban architecture, "
            "a printed color palette strip, and a black marker, "
            "arranged in an organic collage composition suggesting brand world-building, "
            "creative editorial aesthetic, dramatic directional lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "09",
        "title": "商品写真の撮り方",
        "filename": "09_product-photography.png",
        "concept": "A. 商品・素材フォーカス型",
        "prompt": (
            "A smartphone on a small tripod pointed at a flat-laid streetwear hoodie on a concrete floor, "
            "with a white foam reflector board leaning nearby and soft natural window light, "
            "suggesting DIY product photography setup for apparel, "
            "clean minimal aesthetic, natural warm daylight atmosphere, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "10",
        "title": "SNS集客 Instagram",
        "filename": "10_sns-instagram.png",
        "concept": "C. ストリートカルチャー型",
        "prompt": (
            "Smartphone lying on dark concrete showing a clean, cohesive streetwear brand Instagram grid layout, "
            "surrounded by a folded t-shirt, earphones, and a coffee cup, "
            "urban lifestyle aesthetic with warm ambient lighting, "
            "suggesting social media brand building for a street fashion label, "
            "high-resolution commercial photography, shallow depth of field, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "11",
        "title": "ECプラットフォーム比較",
        "filename": "11_ec-platform.png",
        "concept": "D. インフォグラフィック型",
        "prompt": (
            "Laptop computer open on a dark desk displaying an online streetwear store product page, "
            "beside a small cardboard shipping box, a folded t-shirt with a hang tag, and a credit card, "
            "suggesting e-commerce setup for an apparel brand, "
            "clean minimal workspace aesthetic, cool blue monitor glow, soft side lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "12",
        "title": "価格設定",
        "filename": "12_pricing.png",
        "concept": "D. インフォグラフィック型",
        "prompt": (
            "Overhead flat lay on dark surface: a folded streetwear t-shirt with a blank hang tag, "
            "a simple calculator, an open notebook with handwritten pricing columns and percentage symbols, "
            "and a pen, minimal and analytical composition suggesting apparel pricing strategy, "
            "clean urban workspace aesthetic, soft even lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "13",
        "title": "AI活用入門",
        "filename": "13_ai-tools-intro.png",
        "concept": "B. 作業・工程フォーカス型",
        "prompt": (
            "Laptop screen displaying an AI chat interface with a streetwear t-shirt design concept on screen, "
            "beside a sketchbook open to rough clothing design drawings and a stylus, "
            "on a dark creative workspace, blue-toned screen glow against dim ambient light, "
            "suggesting AI-assisted apparel brand creation workflow, "
            "high-resolution commercial photography, sharp focus on screen and sketchbook, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "14",
        "title": "AIでブランドコンセプト",
        "filename": "14_ai-brand-concept.png",
        "concept": "C. ストリートカルチャー型",
        "prompt": (
            "Split composition on dark concrete: left side shows a laptop with colorful AI-generated streetwear "
            "design concepts on screen, right side shows physical mood board with color swatches and fabric samples, "
            "connected visually by a single pen bridging both sides, "
            "suggesting the bridge between AI creativity and physical brand building, "
            "cinematic lighting with screen glow and warm spot, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
    {
        "id": "15",
        "title": "0→1→10 ロードマップ",
        "filename": "15_roadmap.png",
        "concept": "D. インフォグラフィック型",
        "prompt": (
            "Overhead flat lay on dark concrete floor showing a visual progression of apparel brand growth: "
            "far left a single phone with a print-on-demand app, center a small stack of 20 folded t-shirts "
            "with a hang tag, far right a larger stack of 50+ garments in poly bags ready to ship, "
            "arranged in a clear left-to-right progression with arrows made of tape between groups, "
            "industrial warehouse aesthetic, dramatic overhead lighting, "
            "high-resolution commercial photography, sharp focus, "
            "16:9 aspect ratio, no text overlay, no watermark, no faces, no brand logos"
        ),
    },
]

def main():
    print("=== apparel-note アイキャッチ画像 一括生成 ===\n")
    results = []
    for article in ARTICLES:
        print(f"[{article['id']}] {article['title']} ({article['concept']})")
        print(f"  ファイル名: {article['filename']}")
        path = generate_image(article["prompt"], article["filename"])
        results.append({**article, "path": path, "ok": path is not None})
        print()

    print("=== 完了サマリー ===")
    for r in results:
        status = "✓" if r["ok"] else "✗"
        print(f"  {status} [{r['id']}] {r['title']} → {r['filename']}")

    if not all(r["ok"] for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main()
