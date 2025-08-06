import os
import re
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def should_translate(text):
    """Check if text should be translated (exclude numbers, symbols, etc.)"""
    # Remove whitespace
    text = text.strip()
    
    # Skip if empty or too short
    if len(text) < 2:
        return False
    
    # Skip if mostly numbers or symbols
    letter_count = len(re.findall(r'[A-Za-z\u0600-\u06FF\u4e00-\u9fff\u0900-\u097F]', text))
    total_count = len(text)
    
    # Only translate if at least 70% are letters (more strict)
    if letter_count / total_count < 0.7:
        return False
    
    # Skip if text looks garbled (too many repeated characters)
    if len(set(text)) < len(text) * 0.3:  # Less than 30% unique characters
        return False
    
    return True

def translate_text(text, target_lang="en"):
    if not text.strip():
        return ""
    
    # Check if text should be translated
    if not should_translate(text):
        print(f"Skipping translation for: '{text}' (numbers/symbols)")
        return text  # Return original text for numbers/symbols
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Language mapping for prompts
        lang_names = {
            "en": "English",
            "ar": "Arabic", 
            "fr": "French",
            "es": "Spanish",
            "de": "German",
            "zh": "Chinese",
            "hi": "Hindi"
        }
        
        target_language = lang_names.get(target_lang, "English")
        
        print(f"Translating: '{text}' to {target_language}")
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a precise translator. Translate text to {target_language}. Return ONLY the translated text with no explanations, no additional words, no comments. If the text cannot be translated or is garbled, return the original text unchanged."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.0,
            max_tokens=100
        )
        
        translated = completion.choices[0].message.content.strip()
        
        # Clean up the response - remove any explanatory text
        if "translation" in translated.lower() or "translate" in translated.lower():
            # If response contains explanatory text, try to extract just the translation
            lines = translated.split('\n')
            for line in lines:
                line = line.strip()
                if line and not any(word in line.lower() for word in ['translation', 'translate', 'not valid', 'cannot']):
                    translated = line
                    break
        
        # If translation is too long compared to original, likely contains explanation
        if len(translated) > len(text) * 3:
            print(f"Translation too long, using original: '{text}'")
            return text
        
        print(f"Translation result: '{translated}'")
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails