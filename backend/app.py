from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageOps
import pdf2image
import tempfile
import io
import os
from ocr import extract_text_with_boxes
from translate import translate_text
from render_translated import render_translated_text
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"  # Update if your path is different

# Map frontend language code to Tesseract language code
TESSERACT_LANG_MAP = {
    "en": "eng",
    "ar": "ara",
    "fr": "fra",
    "es": "spa",
    "de": "deu",
    "zh": "chi_sim",
    "hi": "hin",
    # Add more as needed
}

# Preprocess image for better OCR
def preprocess_image(img):
    gray = img.convert('L')
    enhanced = ImageOps.autocontrast(gray)
    bw = enhanced.point(lambda x: 0 if x < 128 else 255, '1')
    return bw.convert('RGB')

@app.route("/api/translate", methods=["POST"])
def translate_document():
    logging.info("Received /api/translate request")
    if 'file' not in request.files:
        logging.error("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    target_lang = request.form.get("target_lang", "en")
    output_format = request.form.get("output_format", "image")
    logging.info(f"File received: {file.filename}, Target language: {target_lang}, Output format: {output_format}")

    # Convert PDF to images if needed
    try:
        if file.filename.lower().endswith(".pdf"):
            with tempfile.TemporaryDirectory() as path:
                logging.info("Converting PDF to images...")
                images = pdf2image.convert_from_bytes(file.read(), output_folder=path, poppler_path=POPPLER_PATH, dpi=300)
                images = [img.convert("RGB") for img in images]
                images[0].save("debug_page1.png")
        else:
            logging.info("Opening image file...")
            images = [Image.open(file.stream).convert("RGB")]
    except Exception as e:
        logging.exception("Error during file conversion")
        return jsonify({"error": f"File conversion failed: {str(e)}"}), 500

    rendered_images = []
    for idx, img in enumerate(images):
        try:
            logging.info(f"Preprocessing image for OCR on page {idx+1}...")
            pre_img = preprocess_image(img)
            tesseract_lang = TESSERACT_LANG_MAP.get(target_lang, "eng")
            logging.info(f"Running OCR on page {idx+1} with lang={tesseract_lang}...")
            ocr_results = extract_text_with_boxes(pre_img, lang=tesseract_lang)
            logging.info(f"OCR found {len(ocr_results)} text blocks")
            
            # Print OCR results for debugging
            for i, item in enumerate(ocr_results):
                logging.info(f"OCR Block {i+1}: '{item['text']}' (confidence: {item.get('confidence', 'N/A')})")
            
            # Translate each text block
            for item in ocr_results:
                original_text = item['text']
                item['translated'] = translate_text(original_text, target_lang)
                logging.info(f"Translated: '{original_text}' -> '{item['translated']}'")
            
            logging.info(f"Translation complete for page {idx+1}")
            rendered_img = render_translated_text(img, ocr_results, font_size=28)
            rendered_images.append(rendered_img)
        except Exception as e:
            logging.exception(f"Error processing page {idx+1}")
            return jsonify({"error": f"Processing failed on page {idx+1}: {str(e)}"}), 500

    try:
        if output_format == "pdf":
            logging.info("Saving output as PDF")
            pdf_bytes = io.BytesIO()
            rendered_images[0].save(
                pdf_bytes, format="PDF", save_all=True, append_images=rendered_images[1:]
            )
            pdf_bytes.seek(0)
            return send_file(
                pdf_bytes,
                mimetype="application/pdf",
                as_attachment=True,
                download_name="translated.pdf"
            )
        else:
            logging.info("Saving output as PNG")
            img_bytes = io.BytesIO()
            rendered_images[0].save(img_bytes, format="PNG")
            img_bytes.seek(0)
            return send_file(
                img_bytes,
                mimetype="image/png",
                as_attachment=True,
                download_name="translated.png"
            )
    except Exception as e:
        logging.exception("Error saving or sending output file")
        return jsonify({"error": f"Output failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)