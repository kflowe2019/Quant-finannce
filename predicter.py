from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch import nn
import torch  

# Loads or downloads the FinBERT AI model, the tokenizer, and the neural network model
print("🧠 Loading the FinBERT AI model...")
model_name = "prosusai/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(headline):
    # Does the tokenizing thingy, which converts the text to numbers the AI can understand and stored it into "input"
    inputs = tokenizer(headline, padding=True, truncation=True, return_tensors='pt')
    
    # Uses softmax from the scores of the input to turn those scores into a probablility distribution
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Finds the highest probability, uses argmax to turn them into "binary?" values to assign the score to a prediction label
    labels = ['Positive', 'Negative', 'Neutral']
    score_idx = torch.argmax(predictions)
    label = labels[score_idx]
    confidence = predictions[0][score_idx].item() # Confidence percentage
    
    return label, confidence # tuple

if __name__ == "__main__":
    # Test if the scraper and the model is working correctly
    test_headline = "Asia-Pacific markets mostly rise on hopes for Hormuz reopening"
    label, conf = analyze_sentiment(test_headline)
    print(f"\nHeadline: {test_headline}")
    print(f"AI Sentiment: {label} ({conf:.2%} confidence)")