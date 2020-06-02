import sqlite3


def initialize_databases():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (category_id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keywords
                 (category_id INTEGER, key text, FOREIGN KEY (category_id)
       REFERENCES categories (category_id)) ''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchased_items
                 (date text, item_name text, price real , category_id INTEGER, FOREIGN KEY (category_id)
       REFERENCES categories (category_id))''')
    conn.commit()
    conn.close()


def add_purchased_items(purchases):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    for item in purchases:
        query = "INSERT OR IGNORE INTO purchased_items VALUES ('{0}', '{1}', {2}, {3})".format(item[0], item[1], item[2], item[3])
        print(query)
        c.execute(query)
    conn.commit()
    conn.close()


def get_uncategorized_items():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    query = "SELECT * FROM purchased_items WHERE category_id = -1"
    result = c.execute(query).fetchall()
    conn.commit()
    conn.close()
    return result


def create_new_category(category_name, keywords):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("INSERT INTO categories (name) VALUES ('{0}');".format(category_name))
    category_id = c.execute("SELECT category_id FROM categories WHERE name='{0}'".format(category_name)).fetchone()

    for k in keywords.split(","):
        query = "INSERT INTO keywords VALUES ({0}, '{1}')".format(category_id[0], k.lower())
        c.execute(query)
    conn.commit()
    conn.close()
    return category_id[0]


def update_item_category(item, category_id):

    query = "UPDATE purchased_items SET category_id = {0} WHERE date = '{1}' AND item_name = '{2}'".format(category_id, item[0], item[1])
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def get_all_categories():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    result = c.execute("SELECT * FROM categories").fetchall()
    conn.commit()
    conn.close()
    return result


def update_category(category_id, name, keywords):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    if name != '':
        query = "UPDATE categories SET name = '{0}' where category_id = {1}".format(name, category_id)
        c.execute(query)
    keyword_list = keywords.split(",")
    for key in keyword_list:
        query = "UPDATE keywords SET key = '{0}' where category_id = {1}".format(key.lower(), category_id)
        c.execute(query)
    conn.commit()
    conn.close()


def get_all_keywords(category_id):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    query = "SELECT * FROM keywords WHERE category_id = {0}".format(category_id)
    keywords = c.execute(query).fetchall()
    conn.commit()
    conn.close()
    return keywords


def _get_all_purchased_items():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    result = c.execute("SELECT * from purchased_items").fetchall()
    conn.commit()
    conn.close()
    return result


if __name__ == "__main__":
    print(_get_all_purchased_items())