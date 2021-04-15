from downloader.review_helper import ReviewHelper
from downloader.product_helper import ProductHelper
from downloader.download_helper import DownloadHelper

from datetime import datetime

class Downloader():

    def __init__(self):
        pass

    def run(self, database_location):

        print("---------------  Downloading data --------------------")
        start_time = datetime.now()
        review_source = "http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/Pet_Supplies.json.gz"
        product_source = "http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/meta_Pet_Supplies.json.gz"
        dh = DownloadHelper()
        dh.download(review_source, product_source)
        print("Time to download and decompress: {}".format(datetime.now()-start_time))
        print("Finished.")

        print("---------------  Processing reviews --------------------")
        rh = ReviewHelper()
        rh.create_db_connection(database_location)
        rh.drop_review_table_sql()

        print("Table Dropped.")
        rh.create_review_table_sql()
        print("Table Created.")
        rh.DEBUG = False
        print("Reading data...")
        with open("reviews.json", "r") as reviews:
            review_lines = reviews.readlines()
        print("Found {} reviews.".format(len(review_lines)))
        print("Inserting reviews...")
        rh.insert_json_lines(review_lines)
        print("Creating index.  Be patient.")
        rh.create_index()
        rh.close_db()
        print("Total reviews imported: {}".format(len(review_lines)))

        print("---------------  Processing products --------------------")
        ph = ProductHelper()
        ph.create_db_connection(database_location)
        ph.drop_product_table()
        print("Table Dropped.")
        ph.create_product_table()
        print("Table Created.")
        ph.DEBUG = False
        print("Reading data...")
        with open("products.json", "r") as products:
            product_lines = products.readlines()
        print("Found {} products.".format(len(product_lines)))
        print("Inserting products...")
        ph.insert_json_lines(product_lines)
        print("Creating index.  Be patient.")

        ph.create_index()
        ph.close_db()
        print("Total product imported: {}".format(len(product_lines)))

        print("Data download complete.")
        print("Full time to import data: {}".format(datetime.now() - start_time))
