import requests
import base64
import os
import sys
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY")
OUTPUT_PATH = os.path.expanduser("~/Documents/apparel-note-project-/output/images/")
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

def generate_image(prompt, filename):
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
        return
    image_data = data["predictions"][0]["bytesBase64Encoded"]
    image_bytes = base64.b64decode(image_data)
    filepath = os.path.expanduser(OUTPUT_PATH + filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    print(f"保存完了: {filepath}")

if len(sys.argv) >= 3:
    generate_image(sys.argv[1], sys.argv[2])
else:
    print("使い方: python3 generate.py 'プロンプト' 'ファイル名.png'")
