from downloader.download_helper import DownloadHelper
from unittest import TestCase

class TestDownloadHelper(TestCase):

    def test_download(self):
        dh = DownloadHelper()
        test_reviews = "http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/Electronics.json.gz"
        test_products = "http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/meta_Electronics.json.gz"
        dh.download(test_reviews, test_products)



