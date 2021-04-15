import json
import sqlite3

class ProductHelper:
    DEBUG = False
    CONN = None

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

    def default_get(self, j, s):
        result = "na"
        try:
            result = j[s]
        except Exception as exp:
            self.debug_print("Error parsing {} from {}".format(s, j))
        return result

    def flatten_data(self, j, s):
        flat = "na"
        try:
            flat = ",".join(j[s])
        except Exception as exp:
            self.debug_print("Unable to flatten {}".format(j))
        return flat


    def insert_product_from_json(self, json_string):
        the_json = json.loads(str(json_string))
        category = self.flatten_data(the_json, "category")
        tech1 = self.default_get(the_json, "tech1")
        description = self.flatten_data(the_json, "description")
        fit = self.default_get(the_json, "fit")
        title = self.default_get(the_json, "title")
        also_buy = self.flatten_data(the_json, "also_buy")
        image = self.flatten_data(the_json, "image")
        tech2 = self.default_get(the_json, "tech2")
        brand = self.default_get(the_json, "brand")
        feature = self.flatten_data(the_json, "feature")
        rank = self.flatten_data(the_json, "rank")
        also_view = self.flatten_data(the_json, "also_view")
        similar_item = self.default_get(the_json, "similar_item")
        date = self.default_get(the_json, "date")
        price = self.default_get(the_json, "price").replace("$","")
        asin = self.default_get(the_json, "asin")
        sql = "insert into products values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

        fields = [
        category,
        tech1,
        description,
        fit,
        title,
        also_buy,
        image,
        tech2,
        brand,
        feature, rank, also_view, similar_item, date, price, asin]
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
            self.insert_product_from_json(r_json)
        self.CONN.commit()


    def create_product_table(self):
        sql = """create table products (
        category text,
        tech1 text,
        description text,
        fit text,
        title text,
        also_buy text,
        image text,
        tech2 text,
        brand text,
        feature text, 
        rank text, 
        also_view text, 
        similar_item text, 
        date text, 
        price text, 
        asin text);
        """
        self.CONN.execute(sql)
        self.CONN.commit()

    def create_index(self):
        self.CONN.execute("drop index if exists products_asin_index;")
        self.CONN.execute("create index products_asin_index on products(asin);")
        self.CONN.commit()

    def drop_product_table(self):
        self.CONN.execute("drop index if exists products_asin_index;")
        sql = "drop table if exists products;"
        self.CONN.execute(sql)
        self.CONN.commit()
