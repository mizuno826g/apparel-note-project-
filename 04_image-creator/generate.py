import requests
import base64
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.environ.get("GOOGLE_AI_API_KEY")
OUTPUT_PATH = Path.home() / "Documents/apparel-note-project-/output/images"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, filename):
    if not API_KEY:
        print("エラー: GOOGLE_AI_API_KEY が設定されていません。.env ファイルを確認してください。")
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
        }
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if "error" in data:
        print(f"エラー: {data['error']}")
        return None
    image_data = data["predictions"][0]["bytesBase64Encoded"]
    image_bytes = base64.b64decode(image_data)
    filepath = OUTPUT_PATH / filename
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    print(f"保存完了: {filepath}")
    return str(filepath)

if len(sys.argv) >= 3:
    generate_image(sys.argv[1], sys.argv[2])
else:
    print("使い方: python3 generate.py 'プロンプト' 'ファイル名.png'")
