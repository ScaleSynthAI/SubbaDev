import os
import urllib.request

FONT_DIR = "themes/subba/static/fonts"
os.makedirs(FONT_DIR, exist_ok=True)

FONTS = {
    "inter-latin-400-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/inter/files/inter-latin-400-normal.woff2",
    "inter-latin-500-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/inter/files/inter-latin-500-normal.woff2",
    "inter-latin-600-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/inter/files/inter-latin-600-normal.woff2",
    "source-serif-4-latin-400-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/source-serif-4/files/source-serif-4-latin-400-normal.woff2",
    "source-serif-4-latin-600-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/source-serif-4/files/source-serif-4-latin-600-normal.woff2",
    "jetbrains-mono-latin-400-normal.woff2": "https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2"
}

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in FONTS.items():
    dest = os.path.join(FONT_DIR, name)
    print(f"Downloading {name}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(dest, 'wb') as f:
                f.write(response.read())
        print(f"  Successfully downloaded to {dest}")
    except Exception as e:
        print(f"  Error downloading {name}: {e}")

print("Font downloads complete.")
