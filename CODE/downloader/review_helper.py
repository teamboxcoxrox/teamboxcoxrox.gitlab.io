import json
import sqlite3

class ReviewHelper:

    DEBUG=False
    CONN=None

    def create_db_connection(self, filename):
        print("Creating database connection: {}".format(filename))
        self.CONN = sqlite3.connect(filename)
        assert self.CONN is not None, "Database connection appears to be invalid."

    def debug_print(self, s):
        if self.DEBUG:
            print(s)

    def close_db(self):
        try:
            self.CONN.close()
        except Exception as exp:
            self.debug_print("Failed to close db connection.")

    def default_get(self, j, s):
        result = "na"
        try:
            result = j[s]
        except Exception as exp:
            self.debug_print("Error parsing {} from {}".format(s, j))
        except KeyError as ke:
            self.debug_print("Missing key: {} in {}".format(s, j))
        return result

    def insert_review_from_json(self, json_string):
        the_json = json.loads(str(json_string))
        overall = self.default_get(the_json, 'overall')
        vote = self.default_get(the_json, "vote")
        verified = self.default_get(the_json, 'verified')
        review_time = self.default_get(the_json, "reviewTime")
        reviewer_id = self.default_get(the_json, "reviewerID")
        asin = self.default_get(the_json, "asin")
        reviewer_name = self.default_get(the_json, "reviewerName")
        review_text = self.default_get(the_json, 'reviewText')
        review_summary = self.default_get(the_json, "summary")
        unixReview_time = self.default_get(the_json, "unixReviewTime")
        sql = "insert into reviews values (?,?,?,?,?,?,?,?,?,?);"\

        fields = [
            overall,
            vote,
            verified,
            review_time,
            reviewer_id,
            asin,
            reviewer_name,
            review_text,
            review_summary,
            unixReview_time
        ]
        self.CONN.execute(sql, fields)

    def insert_json_lines(self, json_lines):
        percentage = int(len(json_lines) / 100)

        cnt = 0
        for r_json in json_lines:
            cnt = cnt + 1
            if cnt % percentage == 0:
                self.debug_print("{}% complete.".format(int(cnt / percentage)))
            if cnt % 10000 == 0:
                self.CONN.commit()
                self.debug_print("Checkpoint.")
            self.insert_review_from_json(r_json)
        self.CONN.commit()

    def create_review_table_sql(self):
        sql = """create table reviews (
                overall integer,
                vote integer,
                verified integer,
                review_time text,
                reviewer_id text,
                asin text,                
                reviewer_name text,
                review_text text,
                review_summary text,
                unixReview_time integer);                
        """
        self.CONN.execute(sql)

    def commit(self):
        self.CONN.commit()

    def create_index(self):
        self.CONN.execute("drop index if exists reviews_asin_index;")
        self.CONN.execute("create index reviews_asin_index on reviews(asin)")
        self.CONN.commit();

    def drop_review_table_sql(self):
        self.CONN.execute("drop index if exists reviews_asin_index;")
        sql = "drop table if exists reviews;"
        self.CONN.execute(sql)
