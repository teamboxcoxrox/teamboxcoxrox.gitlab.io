from unittest import TestCase
from bcr_LDA import BCR_LDA
import pandas as pd

class Test_BCRLDA(TestCase):

    def test_clean_text(self):
        bcr = BCR_LDA()
        text = 'Monkey jupyter alexander great text fish cat good great in it which is great alpha great'
        text = bcr.clean_text(text)
        print(text)
        self.assertNotIn('great', text)

    def test_aggregate(self):
        data = [['123', 'some text'],['123', 'some more text'], ['123', 'evn more text'],
                ['456', 'some stuff'],['456', 'some more stuff'], ['456', 'even more stuff'],
                ['789','just a little thing.']]

        df = pd.DataFrame(data=data, columns=['asin','review_text'])
        bcr = BCR_LDA()
        result = bcr.aggregate_df(df, 'asin', 'review_text')
        # This should aggregate to only three rows.
        self.assertEqual(len(result),3)
        print(result)

    def test_there_is_data(self):
        bcr = BCR_LDA()
        categories, category_ids, asin_counts = bcr.get_categories('category.csv')
        i = 0
        for category in categories:
            asin_count = asin_counts[i]
            i = i + 1
            dataset = bcr.get_dataset('category.csv', category)
            print("Dataset {} has {} records.".format(category, len(dataset)))
            self.assertEqual(len(dataset), asin_count)
            print("Displaying the first 10 elements in the dataset...")
            print(dataset.head(10))