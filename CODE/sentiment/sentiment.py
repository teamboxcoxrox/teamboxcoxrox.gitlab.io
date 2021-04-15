import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

class Sentiment:

    def run(self, database_file):
        print("Starting sentiment analysis...")
        start_time = datetime.now()
        # Create your connection
        cnx = sqlite3.connect(database_file)

        # Use the below to check table names
        df = pd.read_sql_query("select name from sqlite_master where type = 'table'", cnx)
        # df.iloc[:5]

        # Pull product and reviews table
        df_rev = pd.read_sql_query("select * from reviews", cnx)
        # df_prod = pd.read_sql_query("select * from products", cnx)

        # Build initial sentiment dataframe
        df_sentiment = df_rev[['asin', 'review_text']].copy()

        # Score each review in dataset
        analyzer = SentimentIntensityAnalyzer()

        # Add compound score (normalized between -1 and 1)
        df_sentiment['sentiment_score'] = [analyzer.polarity_scores(v)['compound'] for v in df_sentiment['review_text']]

        # Write Sentiment to CSV
        df_sentiment.to_csv(r"pets_sentiment.csv")

        # Aggregate asin by summary statistics
        df_sentiment_grouped = df_sentiment.groupby('asin')['sentiment_score'].agg(
            {'mean', 'median', 'std', 'max', 'min'}).reset_index()

        # Write Group to CSV
        df_sentiment_grouped.to_csv(r"pets_sentiment_grouped.csv")

        print("Sentiment analysis complete.  Elapsed time: {}".format(datetime.now() - start_time))