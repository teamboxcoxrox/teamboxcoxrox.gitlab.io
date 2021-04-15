from unittest import TestCase
from downloader.product_helper import ProductHelper



class TestProductHelper(TestCase):

    def test_review_helper(self):
        ph = ProductHelper()
        conn = ph.create_db_connection("electronics_test.db")
        ph.drop_product_table_sql()
        ph.create_product_table_sql()
        with open("test_product.json", "r") as f:
            r_json = f.readlines()
        ph.insert_product_from_json(r_json[0])
        cur = ph.CONN.cursor()
        cur.execute("Select count(*) from products;")
        rows = cur.fetchall()
        c = rows[0][0]
        self.assertEqual(1, c)
        ph.close_db()