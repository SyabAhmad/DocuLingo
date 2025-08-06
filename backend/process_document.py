from PIL import Image
import pdf2image
import tempfile
import os
from ocr import extract_text_with_boxes
from translate import translate_text
from render_translated import render_translated_text

def process_document(file_path, target_lang="en", output_format="image"):
    """
    Processes a document (PDF or image), translates, and renders the result.
    Returns the output file path.
    """
    if file_path.lower().endswith(".pdf"):
        with tempfile.TemporaryDirectory() as path:
            images = pdf2image.convert_from_path(file_path, output_folder=path)
            images = [img.convert("RGB") for img in images]
    else:
        images = [Image.open(file_path).convert("RGB")]

    rendered_images = []
    for img in images:
        ocr_results = extract_text_with_boxes(img)
        for item in ocr_results:
            item['translated'] = translate_text(item['text'], target_lang)
        rendered_img = render_translated_text(img, ocr_results)
        rendered_images.append(rendered_img)

    if output_format == "pdf":
        output_path = "translated_output.pdf"
        rendered_images[0].save(
            output_path, format="PDF", save_all=True, append_images=rendered_images[1:]
        )
    else:
        output_path = "translated_output.png"
        rendered_images[0].save(output_path, format="PNG")
    return output_path

# Example usage:
# result = process_document("input.pdf", target_lang="fr", output_format="pdf")
# print("Saved to:", result)