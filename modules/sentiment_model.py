from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze the sentiment of the input text using TextBlob.
    Returns the polarity score and sentiment label (Positive, Negative, Neutral).
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)

    # Adjust the sentiment thresholds to correctly classify neutral cases
    if polarity > 0.2:
        label = 'Positive'
    elif polarity < -0.2:
        label = 'Negative'
    else:
        label = 'Neutral'  # Neutral when polarity is in the range of -0.1 to 0.1

    print(f"Polarity for text '{text}': {polarity}")  # Debugging print statement

    return polarity, label