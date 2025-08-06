from PIL import ImageDraw, ImageFont, Image
import os

def render_translated_text(image, ocr_results, font_size=32):
    """
    Draws translated text onto the image at the positions of the original text.
    Uses black text with fully opaque white background for better clarity.
    """
    # Create a copy to avoid modifying the original
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    
    # Try to load font with larger size
    font_path = os.path.join(os.path.dirname(__file__), "NotoSans-Regular.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        try:
            # Try system fonts with larger size
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    print(f"Rendering {len(ocr_results)} translated text blocks with font size {font_size}")
    
    # Create overlay for semi-transparent backgrounds
    overlay = Image.new('RGBA', img_copy.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    for item in ocr_results:
        if 'translated' in item and item['translated']:
            x, y = item['left'], item['top']
            width, height = item['width'], item['height']
            translated_text = item['translated']
            
            print(f"Rendering: '{item['text']}' -> '{translated_text}' at ({x}, {y})")
            
            # Calculate text size
            bbox = draw.textbbox((0, 0), translated_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Draw semi-transparent white background (70% opacity for better visibility)
            padding = 4
            overlay_draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill=(255, 255, 255, 255)  # Fully opaque white
            )
    
    # Composite the overlay onto the image
    img_copy = Image.alpha_composite(img_copy.convert('RGBA'), overlay)
    img_copy = img_copy.convert('RGB')
    
    # Now draw the text in black with larger, bolder appearance
    draw = ImageDraw.Draw(img_copy)
    for item in ocr_results:
        if 'translated' in item and item['translated']:
            x, y = item['left'], item['top']
            translated_text = item['translated']
            
            # Draw black text multiple times for bold effect
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    draw.text(
                        (x + dx, y + dy),
                        translated_text,
                        fill=(50, 50, 50),  # Dark gray shadow
                        font=font
                    )
            
            # Draw main black text
            draw.text(
                (x, y),
                translated_text,
                fill=(0, 0, 0),  # Black text
                font=font
            )
    
    print(f"Finished rendering translated text")
    return img_copy