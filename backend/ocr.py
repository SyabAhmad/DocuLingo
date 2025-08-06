import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if your path is different

def extract_text_with_boxes(image, lang="eng"):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang=lang)
    results = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        confidence = int(data['conf'][i])
        
        # Filter: only include text with good confidence and meaningful content
        if confidence > 30 and text and len(text) > 1:
            # Check if text contains meaningful letters (not just numbers/symbols)
            if re.search(r'[A-Za-z\u0600-\u06FF\u4e00-\u9fff\u0900-\u097F]', text):
                results.append({
                    "text": text,
                    "left": data['left'][i],
                    "top": data['top'][i],
                    "width": data['width'][i],
                    "height": data['height'][i],
                    "confidence": confidence
                })
    return results