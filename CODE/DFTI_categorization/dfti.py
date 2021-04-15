import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
from progress.bar import Bar

######################################################################################################################
# Direct Frequency Topic Identification (DFTI)
#
# One of the challenges with using LDA is that it is an unsupervised algorithm. As a result, like PCA, the clusters
# that it discovers may or may not align with desired goals of data scientists. As an example consider the following
# text for review:
#   "My dog really likes this cat food made from fish products. Most dog food he has tried hasn't gone
#   over well with him at all. But this product is really outstanding."
#
# In the above scenario, this text might be classified as either dog, cat or fish. It could also be classified as food
# or product depending on how the LDA system is configured.  As a way to get around this problem, a different approach
# could be used. If, instead of starting with the review text, what if we started with buckets. Such as the following:
#
# [dog cat fish bird rabbit turtle snake rat mouse hamster gerbil reptile horse other]
#
# This code attempts to implement the above algorithm.
#
######################################################################################################################

class DFTI:

    def run(self, database_file):
        start_time = datetime.now()

        CONN = sqlite3.connect(database_file)
        buckets = ['dog', 'cat', 'fish', 'bird', 'amphibians and reptiles', 'rabbits and rodents', 'farm animals']

        words = {
            'dog': ['dog', 'dogs', 'puppy', 'pup', 'puppies', 'paw', 'paws'],
            'cat': ['cat', 'cats', 'kitten', 'kittens', 'feline', 'felines'],
            'fish': ['goldfish', 'fish', 'fishes', 'koi', 'angelfish', 'catfish', 'guppies', 'freshwater', 'saltwater'],
            'bird': ['parrot', 'parrots', 'beak', 'feather', 'beaks', 'feathers', 'bird', 'birds', 'canary', 'canaries',
                     'budgerigar', 'budgerigars', 'budgies', 'parakeets', 'cockatiel', 'cockatiels', 'cockatoo',
                     'cockatoos', 'macaw', 'macaws', 'dove', 'doves'],
            'rabbits and rodents': ['rabbit', 'rabbits', 'bunny', 'bunnies', 'hare', 'hares', 'lop', 'rat', 'mouse',
                                    'hamster', 'gerbil', 'rats', 'mice', 'hamsters', 'gerbils', 'rodents', 'rodent',
                                    'guinea', 'ferret', 'hedgehog', 'ferrets', 'hedgehogs'],
            'farm animals': ['chicken', 'chicks', 'chickens', 'duck', 'ducks', 'goat', 'goats', 'bull', 'cow', 'bulls',
                             'cows', 'lamb', 'sheep', 'sheeps', 'horse', 'pony', 'horses', 'ponies', 'stud', 'mare',
                             'studs', 'mares'],
            'amphibians and reptiles': ['turtle', 'turtles', 'tortoise', 'tortoises', 'tadpole', 'tadpoles', 'cooter',
                                        'loggerhead', 'snapper', 'terrapin', 'leatherback', 'snake', 'snakes', 'gecko',
                                        'geckos', 'lizard', 'lizards', 'frog', 'frogs', 'toad', 'toads', 'amphibian',
                                        'amphibians', 'reptile', 'reptiles', 'snake', 'snakes', 'dragon', 'dragons']
        }

        cur = CONN.cursor()

        cur.execute("SELECT asin from reviews")
        asins = cur.fetchall()
        print("Number of reviews: {}".format(len(asins)))

        cur.execute("SELECT DISTINCT asin from reviews")
        counts = []
        unique_asins = cur.fetchall()
        print("Unique asins found: {}".format(len(unique_asins)))
        start = datetime.now()

        i = 0

        def get_title():
            cur.execute("SELECT asin, title, description from products")
            titles = cur.fetchall()
            results_df = pd.DataFrame(titles)
            results_df.columns = ['asin', 'title', 'description']
            results_df["combined"] = results_df["title"] + results_df["description"]
            result_dict = dict(zip(results_df.asin, results_df.combined))
            return result_dict

        product_description = get_title()

        bar = Bar('Processing', max = len(unique_asins))
        for asin in unique_asins:
            i = i + 1
            bar.next()

            sql = "select review_text from reviews where asin = '{}'".format(asin[0])
            cur.execute(sql)
            rec = [asin[0]]
            full_text = " ".join([x[0] for x in cur.fetchall()])
            if (asin[0] in product_description):
                full_text = full_text + product_description[asin[0]]
            for bucket in buckets:
                cnt = sum(full_text.lower().count(x) for x in words[bucket])
                rec.append(cnt)
            counts.append(rec)

        bar.finish()
        print("Compute time {}".format(datetime.now() - start))

        results_df = pd.DataFrame(counts)

        # display(results_df.head(20))

        def get_max_row(x):
            vals = x.values[1:]
            if max(vals) == 0:
                return -1
            else:
                return (np.argmax(vals))

        def get_category(row, b):
            x = row['category_id']
            if x == -1:
                return "other"
            else:
                return b[x]

        results_df['category_id'] = results_df.apply(lambda row: get_max_row(row), axis=1)
        results_df['category'] = results_df.apply(lambda row: get_category(row, buckets), axis=1)

        results_df.rename(columns={0: 'asin'}, inplace=True)
        results_df = results_df[['asin', 'category_id', 'category']]
        print(results_df.head(10))
        results_df.to_csv('category.csv', index=False)
        results_df.groupby('category').count()

        print("DFTI Categorization complete.")
        print("Elapsed time: {}".format(datetime.now() - start_time))
