import sqlite3

class DB_Manager():

    def __init__(self, database):
        self.database = database

    def execute(self, query):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    """
    x = execute("SELECT title, release_date FROM movies ORDER BY release_date LIMIT 5")
    for i in x:
        print(i[0], "|", i[1])
    """
    def insert_movie(self, data):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute('INSERT OR IGNORE INTO movies (title, budget, popularity, release_date, vote_average, vote_count, overview, tagline, director_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

manager = DB_Manager("movie.db")
manager.insert_movie(tuple(['1', 2, 3, 4/4/4, 5, 6, '7', '8', 7111]))