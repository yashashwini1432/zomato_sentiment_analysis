import re

def clean_text(text):
    """
    Clean the input text by removing all HTML tags.
    """
    # Remove all HTML tags using a regular expression
    cleaned_text = re.sub(r'<.*?>', '', text)
    return cleaned_text
def detect_language(text):
    """
    Detect the language of the input text.
    Returns 'en' for English and 'non-en' for any other language.
    """
    # Simple heuristic for language detection
    # This will be improved later with a proper library like langdetect
    return "en" if all(ord(c) < 128 for c in text) else "non-en"
