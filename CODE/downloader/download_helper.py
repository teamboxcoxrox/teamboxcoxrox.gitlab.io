import os
import urllib.request
import gzip
import shutil


class DownloadHelper:

    def download_file(self, url, fileprefix):
        filename = "{}.gz".format(fileprefix)
        if not os.path.exists(filename):
            urllib.request.urlretrieve(url, filename)
        else:
            print("The requested file seems to have already been downloaded.  "
                  "Please delete {} if you wish to download it again.".format(filename))
        print("File {} has been downloaded.".format(filename))
        return filename

    def decompress_file(self, fileprefix):
        filename_gz = "{}.gz".format(fileprefix)
        filename_json = "{}.json".format(fileprefix)
        if not os.path.exists(filename_json):
            with gzip.open(filename_gz, 'rb') as f_in:
                with open(filename_json, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            print(
                "The target json file {} seems to exist.  "
                "Please delete it if you wish to decompress it again.".format(filename_json))
        print("File {} has been uncompressed.".format(filename_json))


    def download(self, review_file, product_file):
        reviews_archive = self.download_file(review_file, 'reviews')
        self.decompress_file('reviews')

        products_archive = self.download_file(product_file, 'products')
        self.decompress_file('products')

