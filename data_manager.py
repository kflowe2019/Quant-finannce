import pandas as pd
import os

def update_csv_with_sentiment(ticker, sentiment_label, sentiment_score):
    file_path = f"data/{ticker}_history.csv"
    if not os.path.exists(file_path): # does the file not exist?
        return
    
    df = pd.read_csv(file_path) # loads the .csv to a variable
    # Adding the AI's new data (the AI's verdice and the AI's score) to the .csv file
    df.loc[df.index[-1], 'AI_Sentiment_Label'] = sentiment_label
    df.loc[df.index[-1], 'AI_Sentiment'] = sentiment_score
    df.to_csv(file_path, index=False)
    print(f"✅ CSV Updated: {sentiment_label}")