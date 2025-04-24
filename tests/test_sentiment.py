import unittest
from modules.sentiment_model import analyze_sentiment

class TestSentimentModel(unittest.TestCase):

    def test_positive_sentiment(self):
        polarity, label = analyze_sentiment("I love the food!")
        self.assertEqual(label, "Positive")
        self.assertGreater(polarity, 0)

    def test_negative_sentiment(self):
        polarity, label = analyze_sentiment("The food was terrible.")
        self.assertEqual(label, "Negative")
        self.assertLess(polarity, 0)

    def test_neutral_sentiment(self):
        polarity, label = analyze_sentiment("The food was okay.")
        print(f"Neutral test result: Polarity={polarity}, Label={label}")
        # Assert polarity is in the neutral range (more strict neutral range)
        self.assertEqual(label, "Neutral")
        self.assertTrue(-0.1 <= polarity <= 0.1)  # Check if polarity is within the more stringent neutral range

if __name__ == "__main__":
    unittest.main()