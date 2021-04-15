import sqlite3


class RecommendationsHelper:

    DEBUG=False
    CONN=None

    def create_db_connection(self, filename):
        self.CONN = sqlite3.connect(filename)

    def debug_print(self, s):
        if self.DEBUG:
            print(s)

    def close_db(self):
        try:
            self.CONN.close()
        except Exception as exp:
            self.debug_print("Failed to close db connection.")

    def insert_recommendation(self, asin, title, categories, lda_topic=None, sentiment=None, adj_stars=None):
        sql = "insert into recommendations values (?,?,?,?,?,?);"\

        fields = [asin, title, categories, lda_topic, sentiment, adj_stars]
        self.CONN.execute(sql, fields)

    def insert_recommendations(self, recommendations):
        percentage = int(len(recommendations) / 100)

        cnt = 0
        for recommendation in recommendations:
            cnt = cnt + 1
            if cnt % percentage == 0:
                self.debug_print("{}% complete.".format(int(cnt / percentage)))
            if cnt % 10000 == 0:
                self.CONN.commit()
                self.debug_print("Checkpoint.")
            self.insert_recommendation(recommendation)
        self.CONN.commit()

    def create_recommendations_table(self):
        sql = """create table recommendations (
                asin text,
                title text,
                categories text,
                lda_topic integer,
                sentiment float,
                adj_stars float);                
        """
        self.CONN.execute(sql)

    def commit(self):
        self.CONN.commit()

    def create_index(self):
        self.CONN.execute("drop index if exists recommendation_asin_index;")
        self.CONN.execute("create index recommendation_asin_index on recommendations(asin)")
        self.CONN.commit();

    def drop_recommendations_table(self):
        self.CONN.execute("drop index if exists recommendation_asin_index;")
        sql = "drop table if exists recommendations;"
        self.CONN.execute(sql)
