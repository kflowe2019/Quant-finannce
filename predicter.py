from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch import nn
import torch  

# 1. Load the "Brain" (This might take a minute to download the first time)
print("🧠 Loading the FinBERT AI model...")
model_name = "prosusai/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(headline):
    # 2. Convert text to numbers the AI can understand
    inputs = tokenizer(headline, padding=True, truncation=True, return_tensors='pt')
    
    # 3. Ask the AI for its opinion
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # 4. Format the result
    labels = ['Positive', 'Negative', 'Neutral']
    score_idx = torch.argmax(predictions)
    label = labels[score_idx]
    confidence = predictions[0][score_idx].item()
    
    return label, confidence

if __name__ == "__main__":
    # Test it with one of the headlines you just scraped!
    test_headline = "Asia-Pacific markets mostly rise on hopes for Hormuz reopening"
    label, conf = analyze_sentiment(test_headline)
    print(f"\nHeadline: {test_headline}")
    print(f"AI Sentiment: {label} ({conf:.2%} confidence)")