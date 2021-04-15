from unittest import TestCase
from review_helper import ReviewHelper
import sqlite3


class TestReviewHelper(TestCase):

    def test_review_helper(self):
        rh = ReviewHelper()
        conn = rh.create_db_connection("electronics_test.db")
        rh.drop_review_table_sql()
        rh.create_review_table_sql()
        with open("test_review.json", "r") as f:
            r_json = f.readline()
        rh.insert_review_from_json(r_json)
        cur = rh.CONN.cursor()
        cur.execute("Select count(*) from reviews;")
        rows = cur.fetchall()
        c = rows[0][0]
        self.assertEqual(1, c)
        rh.close_db()
