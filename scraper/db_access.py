import argparse
import sqlite3

def get_all(path_to_sqlite):
    conn = sqlite3.connect(path_to_sqlite)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM articles
    ''')

    articles = cursor.fetchall()
    # for article in articles:
    #     print(f"Title: {article[1]}\n {article[3]}")
    #     print()

    conn.commit()
    conn.close()
    return articles

def reset(path_to_sqlite):
    conn = sqlite3.connect(path_to_sqlite)
    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS articles
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            full_link TEXT,
            abstract TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_range(path_to_sqlite, start, end):
    conn = sqlite3.connect(path_to_sqlite)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM articles WHERE id >= ? AND id <= ?
    ''', (start, end))

    articles = cursor.fetchall()
    # for article in articles:
    #     print(f"Title: {article[1]}\n {article[3]}")
    #     print()
    
    conn.commit()
    conn.close()
    return articles

def get_size(path_to_sqlite):
    conn = sqlite3.connect(path_to_sqlite)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM articles
    ''')

    articles = cursor.fetchall()
    # print(len(articles))

    conn.commit()
    conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Access Data from Database")
    parser.add_argument('--all', type = str, help = "Journal Name")
    parser.add_argument('--reset', type = str, help = "Reset the database")
    parser.add_argument('--range', type = str, help = "Range of Articles (Start,End)")
    parser.add_argument('--size', type = str, help = "Size of Articles")
    args = parser.parse_args()

    path_to_sqlite = "articles.sqlite"
    if args.all:
       get_all(path_to_sqlite)
    
    if args.reset:
        reset(path_to_sqlite)

    if args.range:
        start, end = args.range.split(',')
        get_range(path_to_sqlite, start, end)
    
    if args.size:
        get_size(path_to_sqlite)
        

