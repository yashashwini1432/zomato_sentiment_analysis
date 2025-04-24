import unittest
from modules.preprocessing import clean_text, detect_language

class TestPreprocessing(unittest.TestCase):

    def test_language_detection(self):
        """
        Test if the language detected is not English.
        For a Spanish input, the detected language should not be 'en'.
        """
        detected_lang = detect_language("Hola, cómo estás?")
        self.assertNotEqual(detected_lang, "en")  # Expecting a language other than English

    def test_html_cleaning(self):
        """
        Test if HTML tags are removed properly.
        The input string with HTML tags should have the tags removed.
        """
        cleaned_text = clean_text("Great <b>taste</b>!")
        self.assertEqual(cleaned_text, "Great taste!")  # HTML tags should be removed

if __name__ == "__main__":
    unittest.main()