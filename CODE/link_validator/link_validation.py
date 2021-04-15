from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
from datetime import datetime

class LinkValidator:

    def run(self, top_reviews=1000, geckodriver='./link_validator/geckodriver'):
        print("Starting link validation analysis...")
        driver = webdriver.Firefox(executable_path=geckodriver)
        start_time = datetime.now()
        df = pd.read_csv('ranking.csv')
        df = df.sort_values('overall_count', ascending=False)
        df = df[0:top_reviews]
        N = len(df)
        items = []
        for asin in df['asin']:
            try:
                driver.get("http://amazon.com/gp/product/" + asin)
                driver.find_element_by_id("nav-xshop")
                items.append({"asin": asin, 'valid': 1})
            except:
                items.append({"asin": asin, 'valid': 0})

            if len(driver.window_handles) > 1:
                driver.close()

            time.sleep(0.5)

            # if i == 0:
            #     pass
            # elif i % 10 == 0:
        output_df = pd.DataFrame(data=items, columns=['asin', 'valid'])
        output_df.to_csv(r"product_validation.csv", index=False)
        print("Processing complete.  Elapsed time per item: {}".format((datetime.now() - start_time) / N))
