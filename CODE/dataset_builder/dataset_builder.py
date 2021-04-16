import pandas as pd
import re
import sqlite3
from datetime import datetime
import textwrap

class DatasetBuilder:

    def shorten(self,x):
        if type(x) != str:
            x = ""
        if len(x) > 300:
            x = x[:300].rsplit(' ', 1)[0] + ' ...'
        return x

    # wrappoints to add html breaks at the 50 character mark
    def wrap_line(self,x, wrappoint=50):
        # Cannot do stuff over 1000 characters.
        if len(x)>1000:
            x = x[0:1000]

        #  A more efficient way of doing this...
        #out = ' <br>'.join(x[i:i + wrappoint] for i in range(0, len(x), wrappoint))
        out = " <br>".join(textwrap.wrap(x, 50))
        return out

    def get_all_products(self, database):

        # Create your connection
        cnx = sqlite3.connect(database)
        # Pull product and reviews table
        df_prod = pd.read_sql_query("select * from products", cnx)
        return df_prod

    def run(self, database):
        starttime = datetime.now()
        # Specify the paths to the individual files here...
        lda_file = "LDA_Category_Topic.csv"
        sentiment_file = "pets_sentiment_grouped.csv"
        ranking_file = "ranking.csv"
        validation_file = "product_validation.csv"
        blocklist_file = "blocklist.csv"

        print("Blocklist.")
        blocklist = pd.read_csv(blocklist_file, index_col=False)
        print("Asins in blocklist: {}".format(len(blocklist)))

        print("Product")
        product_df = self.get_all_products(database)
        print("Products before de-duplication: {}".format(len(product_df)))
        product_df.drop_duplicates(subset='asin', keep="first", inplace=True)
        print("Products after de-duplication: {}".format(len(product_df)))

        print("Setting amazon category name...")
        product_df['amazon_category'] = product_df['category']
        product_df.drop('category', inplace=True, axis=1)

        print("Loading sentiment...")
        sentiment_df = pd.read_csv(sentiment_file, index_col=0)
        sentiment_df = sentiment_df.rename(
            {'mean': 'mean_sentiment', 'median': 'median_sentiment', 'max': 'max_sentiment', 'std': 'std_sentiment',
             'min': 'min__sentiment'}, axis=1)

        print("Loading ranking...")
        ranking_df = pd.read_csv(ranking_file, index_col=0)
        ranking_df = ranking_df.rename(
            {'overall_average': 'overall_average_ranking', 'overall_count': 'overall_count_ranking',
             'overall_stdev': 'overall_stdev_ranking',
             'average_length_of_review_text': 'ave_length_review_text', 'percentile': 'percentile_ranking'}, axis=1)

        print("Loading Validation...")
        validation_df = pd.read_csv(validation_file)

        print("Loading LDA...")
        lda_df = pd.read_csv(lda_file, header=0)

        print("Merging LDA...")
        all_df = pd.merge(product_df, lda_df, on="asin", how="inner")

        print("Merging sentiment...")
        all_df = pd.merge(all_df, sentiment_df, suffixes=("", "_sentiment"), on="asin", how="inner")

        print("Merging ranking...")
        all_df = pd.merge(all_df, ranking_df, on="asin", suffixes=("", "_ranking"), how="inner")
        all_df = all_df.drop_duplicates()

        def get_val(x):
            if (x == 1 or x == 0):
                return x
            else:
                return 0

        print("Merging validation...")
        all_df = all_df.merge(validation_df, on='asin', how='left')
        all_df['valid_link'] = all_df.apply(lambda row: get_val(row['valid']), axis=1)

        def get_topic_rank_df(topic, df):
            a = df.copy()
            a = a[a['topic_name'] == topic]
            a.sort_values('rank', inplace=True)
            a.reset_index(inplace=True)
            a['topic_rank'] = a.index
            a = a[['asin', 'topic_rank']]
            return a
        print("Columns: ")
        print(all_df.columns)
        print("\n\n")
        #'tech1', 'description', 'fit', 'title', 'also_buy', 'image', 'tech2',
        #'brand', 'feature', 'rank', 'also_view', 'similar_item', 'date',
        #'price', 'asin', 'amazon_category', 'topic', 'topic_name', 'category',
        #'std_sentiment', 'mean_sentiment', 'min__sentiment', 'median_sentiment',
        #'max_sentiment', 'overall_average_ranking', 'overall_count_ranking',
        #'overall_stdev_ranking', 'ave_length_review_text', 'rank_ranking',
        #'percentile_ranking', 'valid', 'valid_link'

        product_prepped = all_df[
            ['asin', 'title', 'description', 'category', 'topic_name', 'mean_sentiment', 'overall_count_ranking',
             'valid']]

        print("Categories present: {}".format(list(set(all_df['category']))))

        # , asin, title, description, category, topic_name, bubble_color, bubble_size, clean_link
        product_prepped.columns = ['asin', 'title', 'description', 'category', 'topic_name', 'bubble_color',
                                   'bubble_size', 'clean_link']  #

        temp_dfs = []

        print("Performing topic ranking...")
        topics = list(set(all_df['topic_name']))
        for topic in topics:
            topic_df = get_topic_rank_df(topic, all_df)
            temp_dfs.append(product_prepped.merge(topic_df, on="asin", how="inner"))

        product_prepped = pd.concat(temp_dfs)

        product_prepped = product_prepped.drop_duplicates()
        print("Categories after topic ranking: {}".format(list(set(all_df['category']))))
        # Remove bad products.
        print("Applying blocklist...")
        print("Product count before blocklist: {}".format(len(product_df)))
        product_prepped = product_prepped[~product_prepped['asin'].isin(blocklist['asin'])]
        #product_prepped.drop_duplicates('asin', keep="first", inplace=True)
        print("Product count after blocklist:  {}".format(len(product_df)))
        print("Categories present are: {}", list(set(product_prepped['category'])))
        # Trim to top 100 products in LDA topic.
        product_prepped.sort_values(['topic_rank'], inplace=True)

        product_prepped = product_prepped[product_prepped['topic_rank'] <= 100]
        #product_prepped = product_prepped.sample(4000)

        print("Product count after top 100 per topic:  {}".format(len(product_prepped)))
        print("Cleaning up product descriptions...")
        product_prepped['title'] = product_prepped.apply(lambda x: self.wrap_line(x['title']), axis=1)
        htmltags = r'<[^<]+?>'
        print("Cleaning product descriptions...")
        product_prepped['description'] = product_prepped['description'].apply(lambda x: re.sub(htmltags, '', str(x).strip('\n')))
        print("Shortening product descriptions...")
        product_prepped['description'] = product_prepped.apply(lambda x: self.shorten(x['description']), axis=1)
        print("Wrapping product description lines...")
        product_prepped['description'] = product_prepped.apply(lambda x: self.wrap_line(x['description']), axis=1)
        product_prepped.to_csv('products_prepped.csv')
        print("Final product aggregation complete.  Elapsed time: {}".format(datetime.now() - starttime))

