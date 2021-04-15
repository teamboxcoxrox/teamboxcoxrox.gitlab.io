import pandas
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from time import time
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from datetime import datetime
import numpy as np
import pyLDAvis
import pyLDAvis.sklearn
import sqlite3
from progress.bar import Bar
import re


## Note:  This class is based on work done by Olivier Grisel <olivier.grisel@ensta.org>,
#         Lars Buitinck, and Chyi-Kwei Yau <chyikwei.yau@gmail.com>
#         License: BSD 3 clause
# https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py

class LDA:

    def __init__(self):
        pass

    STRIP_WORDS = stopwords.words('english') + \
                  ['the', 'good', 'works', 'use', 'great', 'product', 'loves', 'aspacingsm', 'aspacingsmal',
                   'aspacingsmall', 'aspacingtopmini', 'better', 'classaect',
                   'classasect', 'classasection', 'cmcrarpdrvwtxt', 'cute', 'div', 'easy', 'enjoydiv',
                   'enjoy', 'enjoys', 'enjoyed', 'hate', 'hates', 'hated',
                   'favorite', 'good', 'great', 'happy', 'idvideoblockRXMUYLQX', 'ie', 'like', 'love',
                   'loves', 'loved', 'n', 'nice', 'perfect', 'perfectly', 'product', 'quality', 'really',
                   'datahookproductlinklink', 'classalinknor', 'last', 'long', 'time',
                   'datahookproductlinklinked', 'classalinknormal',
                   'recommend', 'ref', 'super', 'typehidden', 'typehiddenclassasect', 'videoblockdivinput',
                   'well', 'work']

    def plot_top_words(self, model, feature_names, n_top_words, title, category="topic"):

        for topic_idx, topic in enumerate(model.components_):
            top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            weights = topic[top_features_ind]

            ax = plt.gca()
            ax.barh(top_features, weights, height=0.7, color='green')
            plt_title = "Topic {}".format(topic_idx+1)
            ax.invert_yaxis()
            ax.tick_params(axis='both', which='major', labelsize=8)
            for i in 'top right left'.split():
                ax.spines[i].set_visible(False)
            #fig.suptitle(title, fontsize=40)
            plt.subplots_adjust(top=0.95, bottom=0.05, wspace=0.90, hspace=0.05)
            plt.savefig("{}_{}.png".format(category.replace(" ", "_"), topic_idx))
            plt.close()
        # plt.show()

    def process_lda(self, dataset, no_features, no_topics, category, plot=False):

        n_samples = len(dataset)

        # For plotting only.
        n_top_words = 10

        t0 = time()

        data_samples = dataset.values

        #print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                        max_features=no_features,
                                        stop_words='english')
        t0 = time()
        tf = tf_vectorizer.fit_transform(data_samples)
        #print("done in %0.3fs." % (time() - t0))

        #print('\n' * 2, "Fitting LDA models with tf features, "
        #                "n_samples=%d and n_features=%d..."
        #      % (n_samples, no_features))
        lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        t0 = time()
        result = lda.fit_transform(tf)
        #print("done in %0.3fs." % (time() - t0))

        tf_feature_names = tf_vectorizer.get_feature_names()

        self.plot_top_words(lda, tf_feature_names, n_top_words, 'Topics in LDA for {}'.format(category), category)
        panel = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer, mds='tsne')
        pyLDAvis.save_html(panel, '{}_lda.html'.format(category))
        return result

    def clean_text(self, row, column):
        try:
            text = row[column]
        except Exception as exp:
            print("Error processing text: {}".format(row))
            return "na"
        if type(text) != str:
            text = str(text)
        text = text.lower()

        text = text.replace(".", " ")
        text = ' '.join([i for i in text.split() if i not in self.STRIP_WORDS])

        if len(text) > 1000:
            text = text[0:1000]

        return text

    def aggregate_df(self, df, key, column):
        df = pd.DataFrame(df.groupby([key])[column].apply(lambda x: ' '.join(x)))
        df['asin'] = df.index
        df['idx'] = [x for x in range(len(df))]
        df = df.set_index('idx')
        df.to_csv("temp_reviews.csv")
        return df

    def get_reviews(self, database):
        start_time = datetime.now()
        # Create your connection
        cnx = sqlite3.connect(database)
        # Pull product and reviews table
        df_rev = pd.read_sql_query("select * from reviews", cnx)
        return df_rev

    def get_dataset(self, database, categories_file, category):

        lda_df = pd.read_csv(categories_file)
        reviews_df = self.get_reviews(database)
        lda_df = lda_df[lda_df['category'] == category]
        asins = lda_df['asin']
        reviews = pd.merge(lda_df, reviews_df, on="asin", how="inner")
        reviews['clean_text'] = reviews.apply(lambda row: self.clean_text(row, 'review_text'), axis=1)
        reviews = self.aggregate_df(reviews, 'asin', 'clean_text')
        dataset = pandas.DataFrame()
        dataset['asins'] = asins
        dataset['clean_text'] = reviews['clean_text']
        return dataset

    def get_categories(self, filename):
        cat_df = pd.read_csv(filename)
        categories_df = cat_df.groupby(['category_id', 'category']).count()
        categories_df.reset_index(inplace=True)
        print("The following categories have been loaded:")
        print(categories_df)
        category_ids = categories_df['category_id']
        categories = categories_df['category']
        asin_count = categories_df['asin']
        return categories, category_ids, asin_count

    def run(self, database='pets.db', categories_file='category.csv'):
        final = None
        sLDA = LDA()
        categories, category_ids, asin_count = sLDA.get_categories(categories_file)

        starttime = datetime.now()
        bar = Bar('\nProcessing LDA', max=len(categories))
        for category in categories:
            bar.next()
            cat_start = datetime.now()
            #print("Working on {}".format(category))

            #print("Loading and preprocessing data.")
            dataset = sLDA.get_dataset(database, categories_file, category)
            #print("Data preprocessing complete. Time: {}".format(datetime.now() - cat_start))

            assert len(dataset) > 0, "There appear to be no products in this dataset."

            dataset = dataset.replace(np.nan, 'none', regex=True)

            documents = dataset['clean_text']
            asins = dataset['asins']
            #print("Starting LDA...")
            results = sLDA.process_lda(documents, 50, 7, category=category, plot=True)
            #print("LDA Complete.")

            #print("Total processing time for {}: {}".format(category, datetime.now() - cat_start))
            topic = [np.argmax(x) for x in results]

            #print("Prepare final dataframe for output")

            temp = pd.DataFrame()
            temp['asin'] = [x for x in asins]
            temp['category'] = [category for x in results]
            temp['topic_name'] = ["{}_{}".format(category, x) for x in topic]

            #print("Saving category file for: {}".format(category))
            if final is None:
                final = temp.copy()
            else:
                final = pd.concat([final, temp])

        bar.finish()
        print("Saving the completed LDA Transformation")
        final.to_csv("LDA_Category_Topic.csv", index=False)

        print("LDA Processing complete.  Elapsed time: {}".format(datetime.now() - starttime))
