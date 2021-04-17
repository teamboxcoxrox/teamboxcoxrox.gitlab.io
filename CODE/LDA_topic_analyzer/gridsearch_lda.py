import pandas as pd
import sqlite3
from datetime import datetime
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import Stemmer  # From pip module PyStemmer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
import numpy as np
from matplotlib import pyplot as plt


class GridSearchLDA:

    def get_reviews(self, database):
        print("Connecting to {} for reviews.  Please be patient.".format(database))
        cnx = sqlite3.connect(database)
        reviews = pd.read_sql_query("select * from reviews", cnx)
        cnx.close()
        return reviews

    def get_products(self, database):
        print("Connecting to {} for products.  Please be patient.".format(database))
        cnx = sqlite3.connect(database)
        products = pd.read_sql_query("select asin, title, description from products", cnx)
        cnx.close()
        return products

    def get_unique_categories(self, categories_file):
        cat_df = pd.read_csv(categories_file)
        unique_categories = list(set(cat_df['category']))
        return unique_categories

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

    def aggregate_df(self, df, key, column):
        df = pd.DataFrame(df.groupby([key])[column].apply(lambda x: ' '.join(x)))
        df['asin'] = df.index
        df['idx'] = [x for x in range(len(df))]
        df = df.set_index('idx')
        return df

    def gridsearch_lda(self, category_name, category_file, reviews_df, products_df):

        categories = pd.read_csv(category_file)
        cats = categories[categories['category'] == category_name]

        reviews = reviews_df
        products = products_df
        cat_reviews = reviews.merge(cats, on="asin", how="inner")

        cat_reviews = cat_reviews[['asin', 'review_text']]
        cats_df = self.aggregate_df(cat_reviews, 'asin', 'review_text')

        cats_df = cats_df.merge(products, on="asin", how="inner")
        cats_df['all_text'] = cats_df.apply(lambda row: "{} {} {}".format(row['title'],
                                                                          row['description'],
                                                                          row['review_text']),
                                                                          axis=1)

        # Remove non-word characters, so numbers and ___ etc
        cats_df['all_text'] = cats_df['all_text'].str.replace("[^A-Za-z ]", " ")
        dataset = cats_df.sample(2000)

        # English stemmer from pyStemmer
        stemmer = Stemmer.Stemmer('en')

        analyzer = CountVectorizer().build_analyzer()

        # Override TfidfVectorizer
        class StemmedCountVectorizer(CountVectorizer):
            def build_analyzer(self):
                analyzer = super(CountVectorizer, self).build_analyzer()
                return lambda doc: stemmer.stemWords(analyzer(doc))

        vectorizer = StemmedCountVectorizer(stop_words='english', min_df=5, max_df=0.5)
        matrix = vectorizer.fit_transform(dataset['all_text'])

        words_df = pd.DataFrame(matrix.toarray(),
                                columns=vectorizer.get_feature_names())

        # Options to try with our LDA
        # Beware it will try *all* of the combinations, so it'll take ages
        search_params = {
            'n_components': [3, 5, 7, 9, 15],
            'learning_decay': [.5, .7]
        }

        # Set up LDA with the options we'll keep static
        model = LatentDirichletAllocation(learning_method='online')

        # Try all of the options
        gridsearch = GridSearchCV(model, param_grid=search_params, n_jobs=-1, verbose=1)
        gridsearch.fit(matrix)

        # What did we find?
        print("Best Model's Params: ", gridsearch.best_params_)
        print("Best Log Likelihood Score: ", gridsearch.best_score_)
        print("Training final model...")
        n_components = gridsearch.best_params_['n_components']
        learning_decay = gridsearch.best_params_['learning_decay']

        final_lda = LatentDirichletAllocation(learning_method='online',
                                              n_components=n_components,
                                              learning_decay=learning_decay)

        all_matrix = vectorizer.fit_transform(cats_df['all_text'])
        results = final_lda.fit_transform(all_matrix)
        temp = pd.DataFrame()
        topics = np.argmax(results, axis=1)
        temp['asin'] = cats_df['asin']
        temp['topic'] = topics
        temp['topic_name'] = ["{}_{}".format(category_name, x) for x in topics]
        temp['category'] = [category_name for x in results]

        tf_feature_names = vectorizer.get_feature_names()
        self.plot_top_words(final_lda, tf_feature_names, 10, 'Topics in LDA for {}'.format(category_name), category_name)

        return temp

    def run(self, database='pets.db', categories_file='category.csv'):
        final = None
        unique_categories = self.get_unique_categories(categories_file)
        reviews_df = self.get_reviews(database)
        products_df = self.get_products(database)

        starttime = datetime.now()

        for category in unique_categories:
            print("Working on category: {}".format(category))
            temp_df = self.gridsearch_lda(category, categories_file, reviews_df, products_df)

            if final is None:
                final = temp_df.copy()
            else:
                final = pd.concat([final, temp_df])

        print("Saving the completed LDA Transformation")
        final.to_csv("LDA_Category_Topic.csv", index=False)

        print("LDA Processing complete.  Elapsed time: {}".format(datetime.now() - starttime))
