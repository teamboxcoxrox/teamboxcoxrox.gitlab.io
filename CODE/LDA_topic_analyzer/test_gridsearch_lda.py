from unittest import TestCase
from gridsearch_lda import GridSearchLDA
import pandas as pd
from datetime import datetime

class TestGridSearchLDA(TestCase):

    def test_do_it(self):
        starttime = datetime.now()
        gLDA = GridSearchLDA()
        reviews_df = gLDA.get_reviews("../pets.db")
        products_df = gLDA.get_products("../pets.db")
        results_df = gLDA.gridsearch_lda("cat", "../category.csv", reviews_df, products_df)
        results_df.to_csv("cat_test_results.csv")
        print("Run complete.  Elapsed time: {}".format(datetime.now()-starttime))
