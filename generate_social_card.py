import os
from PIL import Image, ImageDraw, ImageFont

def generate_card():
    # 1. Create a high-res 1200x630 image (standard OpenGraph size)
    # Light gray background matching the site's theme (--canvas: #fafafa)
    width = 1200
    height = 630
    background_color = (250, 250, 250)
    
    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # 2. Draw a clean, minimalist accent border
    accent_color = (13, 115, 119) # #0d7377 - Muted Teal
    draw.rectangle([30, 30, width - 30, height - 30], outline=accent_color, width=4)
    
    # 3. Attempt to load system or self-hosted fonts
    # We will search for standard fonts or default to a standard fallback
    font_title = None
    font_sub = None
    
    # Try a few fonts that are commonly installed or easily loadable
    font_paths = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "DejaVuSerif.ttf"
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 64)
                font_sub = ImageFont.truetype(path, 36)
                print(f"Loaded font: {path}")
                break
            except:
                pass
                
    if font_title is None:
        # Fall back to default if no premium font loaded
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        print("Using fallback default font")

    # 4. Draw content
    # Name
    draw.text((100, 180), "Subba Taniparti", fill=(17, 17, 17), font=font_title)
    
    # Title
    draw.text((100, 280), "Lead AI Engineer", fill=(17, 17, 17), font=font_sub)
    
    # Description / Focus
    draw.text((100, 340), "Production ML Systems & MLOps / GenAIOps Platforms", fill=(102, 102, 102), font=font_sub)
    
    # URL & Location Footer
    draw.text((100, 480), "subba.dev  ·  Raleigh-Durham, NC", fill=accent_color, font=font_sub)
    
    # 5. Save the image
    os.makedirs("content/images", exist_ok=True)
    dest_path = "content/images/social_share.png"
    img.save(dest_path)
    print(f"Social card generated successfully at {dest_path}")

if __name__ == "__main__":
    generate_card()
