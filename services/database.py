import sqlite3

def getDatabaseConnection():
    conn = sqlite3.connect('videos.db')
    return conn

def initializeDatabaseTables(connection):
    """
        Create the database.
    """
    c = connection.cursor()

    c.execute('''
        CREATE TABLE types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT
        )''')

    c.execute('''
        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )''')

    c.execute('''
        CREATE TABLE videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            type_id INTEGER,
            game_id INTEGER,
            FOREIGN KEY(type_id) REFERENCES types(id),
            FOREIGN KEY(game_id) REFERENCES games(id)
        )''')

    c.execute("INSERT INTO types VALUES (1, 'day')")
    c.execute("INSERT INTO types VALUES (2, 'week')")
    c.execute("INSERT INTO types VALUES (3, 'month')")

    c.execute("INSERT INTO games VALUES (1, 'fortnite')")

    connection.commit()

def insertClip(connection, title, date, type_id, game_id):
    c = connection.cursor()
    c.execute("insert into videos (title, date, type_id, game_id) values (?, ?, ?, ?)", (title, date, type_id, game_id))
    connection.commit()

def closeConnection(connection):
    connection.close()