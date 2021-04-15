from downloader.downloader import Downloader
from DFTI_categorization.dfti import DFTI
from sentiment.sentiment import Sentiment
from LDA_topic_analyzer.lda import LDA
from dataset_builder.dataset_builder import DatasetBuilder
from ranking.rankings import Rankings
from link_validator.link_validation import LinkValidator
from datetime import datetime

class BoxCoxRoxPipeline:

    dd = Downloader()
    dfti = DFTI()
    sentiment = Sentiment()
    lda = LDA()
    dataset_builder = DatasetBuilder()
    ranking = Rankings()
    validator = LinkValidator()

    database_location = "pets.db"
    categories_file = "category.csv"

    def run(self, download_data=True):
        print("Downloader...")
        if download_data:
            self.dd.run(self.database_location)
        print("DFTI...")
        #self.dfti.run(self.database_location)
        print("Sentiment...")
        #self.sentiment.run(self.database_location)
        print("Ranking...")
        #self.ranking.run(self.database_location)
        print("Validator...")
        #self.validator.run(top_reviews=50)
        print("LDA...")
        #self.lda.run(self.database_location, self.categories_file)
        print("Build Dataset...")
        self.dataset_builder.run(self.database_location)

if __name__ == '__main__':
    starttime = datetime.now()
    bcr = BoxCoxRoxPipeline()
    bcr.run(download_data=False)
    print("Data Pipeline Complete!  Whew!  Total processing time: {}".format(datetime.now()-starttime))




