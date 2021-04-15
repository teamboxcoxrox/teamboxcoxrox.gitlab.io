import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime


class Rankings:

    def run(self, database):
        print("Starting product ranking...")
        start_time = datetime.now()
        conn = sqlite3.connect(database)
        query = conn.execute("SELECT * From reviews")
        cols = [column[0] for column in query.description]
        results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

        print("import completed!")

        #                       Dataframe #1                  #

        # # average "overall" rating grouped by ASIN
        # average_by_asin = results.groupby(['asin'])['overall'].mean().to_frame().reset_index()

        # #average "overall" rating for all ASINs
        # average_overall = results['overall'].mean()

        # # create final dataframe
        # final = average_by_asin
        # final['average_overall'] = average_overall
        # #print(average_by_asin)

        # # show columns
        # #print(list(average_by_asin.columns.values))

        # # Rank (0 being the worst, N being the best) for this ASIN based on ave. overall score
        # final['rank'] = final['overall'].rank(ascending=True, method='dense')
        # #final['rank'] = final['rank']

        # # https://www.geeksforgeeks.org/percentile-rank-of-a-column-in-a-pandas-dataframe/
        # # Percentile (0<= p <=1) for this ASIN. The ASIN with the highest overall will be ranked 1, the lowest ASIN will be ranked 0.
        # final['percentile'] = final['overall'].rank(pct = True)

        # print(final)
        # # write result to csv
        # final.to_csv('output.csv', encoding='utf-8', index=False)

        #                       Dataframe #2                  #

        # average "overall" rating grouped by ASIN
        average_by_asin = results.groupby(['asin'])['overall'].mean().to_frame().reset_index()
        average_by_asin['overall_average'] = average_by_asin['overall']
        average_by_asin = average_by_asin[['asin', 'overall_average']]
        print("average_by_asin completed!")

        # count grouped by ASIN
        count = results.groupby(['asin'])['overall'].count().to_frame().reset_index()
        count['overall_count'] = count['overall']
        count = count[['asin', 'overall_count']]
        print("count completed!")

        # stdev of overall grouped by ASIN
        stdev = results.groupby(['asin'])['overall'].agg(np.std, ddof=0).to_frame().reset_index()
        stdev['overall_stdev'] = stdev['overall']
        stdev = stdev[['asin', 'overall_stdev']]
        print("stdev completed!")

        # length of all of the review texts
        length_of_text = results
        length_of_text['average_length_of_review_text'] = length_of_text['review_text'].str.split().str.len()
        length_of_text = length_of_text[['asin', 'average_length_of_review_text']]
        length_of_text = length_of_text.groupby(['asin'])[
            'average_length_of_review_text'].mean().to_frame().reset_index()
        print("length_of_text completed!")

        # create final dataframe
        final = pd.merge(pd.merge(average_by_asin, count, on='asin'), stdev, on='asin')
        final = final.merge(length_of_text, on='asin')
        print("create final dataframe completed!")

        # # sort by average overall desc, count(*) desc, stdev(*) asc, and text length desc.
        final = final.sort_values(
            ['overall_average', 'overall_count', 'overall_stdev', 'average_length_of_review_text'],
            ascending=[False, False, True, False])

        # # number the rows, and that becomes the rank
        final['rank'] = np.arange(len(final))
        print("rank completed!")
        # print(final)

        # show columns
        # print(list(final.columns.values))

        # https://www.geeksforgeeks.org/percentile-rank-of-a-column-in-a-pandas-dataframe/
        # Percentile (0<= p <=1) for this ASIN. The ASIN with the highest overall will be ranked 1, the lowest ASIN will be ranked 0.
        final = final.reset_index()
        length = len(final)
        final['percentile'] = (len(final) - final['rank']).rank(pct=True)
        print("percentile ranking completed!")

        # print(final)
        # write result to csv
        final.to_csv('ranking.csv', encoding='utf-8', index=False)

        conn.close()
        print("Ranking calculation complete.  Results saved to: {}  Elapsed time: {}".format('ranking.csv',
                                                                                             datetime.now() - start_time))
