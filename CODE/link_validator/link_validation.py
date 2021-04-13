from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
import sqlite3
from datetime import datetime

print("Starting sentiment analysis...")
driver = webdriver.Firefox(executable_path=r"./geckodriver")
start_time = datetime.now()
tart_time = datetime.now()
conn = sqlite3.connect('../pets_all.db')
query = conn.execute("SELECT * From products limit 20")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
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
