from unittest import TestCase
from dataset_builder.recommendations_helper import RecommendationsHelper

class TestRecommendationsHelper(TestCase):

    def test_recommendations_stuff(self):

        recHelper = RecommendationsHelper();
        recHelper.create_db_connection("electronics_test.db")
        recHelper.drop_recommendations_table()
        recHelper.create_recommendations_table()

        recHelper.insert_recommendation(asin='123test', title='mock product', categories='blah blah blah')
        cur = recHelper.CONN.cursor()
        cur.execute("Select * from recommendations;")
        rows = cur.fetchall()
        print(rows)
        cur.execute("Select count(*) from recommendations;")
        rows = cur.fetchall()
        c = rows[0][0]
        print(c)
        self.assertEqual(1, c)
        recHelper.close_db()



