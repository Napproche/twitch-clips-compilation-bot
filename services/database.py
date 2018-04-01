import sqlite3

import constants

def getDatabaseConnection():
    conn = sqlite3.connect(constants.DATABASE_LOCATION)
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
            name TEXT,
            full TEXT
        )''')

    c.execute('''
        CREATE TABLE channels (
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
            channel_id INTEGER,
            FOREIGN KEY(type_id) REFERENCES types(id),
            FOREIGN KEY(game_id) REFERENCES games(id),
            FOREIGN KEY(channel_id) REFERENCES channels(id)
        )''')

    c.execute("INSERT INTO types VALUES (1, 'day')")
    c.execute("INSERT INTO types VALUES (2, 'week')")
    c.execute("INSERT INTO types VALUES (3, 'month')")

    c.execute("INSERT INTO games VALUES (1, 'Fortnite', 'Fortnite')")
    c.execute("INSERT INTO games VALUES (2, 'Overwatch', 'Overwatch')")
    c.execute("INSERT INTO games VALUES (3, 'League_of_Legends', 'League of Legends')")
    c.execute("INSERT INTO games VALUES (4, 'Hearthstone', 'Hearthstone')")
    c.execute("INSERT INTO games VALUES (5, 'Counter-Strike:_Global_Offensive', 'Counter-Strike: Global Offensive')")
    c.execute("INSERT INTO games VALUES (6, 'PLAYERUNKNOWN%S1S_BATTLEGROUNDS', 'PLAYERUNKNOWNS BATTLEGROUNDS')")
    c.execute("INSERT INTO games VALUES (7, 'StarCraft_II', 'StarCraft II')")
    c.execute("INSERT INTO games VALUES (8, 'Dota_2', 'Dota 2')")
    c.execute("INSERT INTO games VALUES (9, 'Rocket_League', 'Rocket League')")

    connection.commit()

def getChannel(connection, channel):
    """
        Checks if a channel exists. If it does, it will return the information.
        If it doesn't exist, it will create a new channel and return this record.
    """
    instance = doesChannelExist(connection, channel)
    if instance:
        return instance
    else:
        return createChannel(connection, channel)

def doesChannelExist(connection, channel):
    """
        Return True if the channel already exists, False if not.
    """
    c = connection.cursor()
    channel = c.execute('SELECT * FROM channels WHERE name=?', (channel,)).fetchone()
    return channel if channel else None

def createChannel(connection, channel):
    """
        Create a new channel.
    """
    c = connection.cursor()
    c.execute("insert into channels (name) values (?)", (channel, ))
    channel = c.execute('SELECT * FROM channels WHERE name=?', (channel,)).fetchone()
    connection.commit()
    return channel

def getGame(connection, game):
    c = connection.cursor()
    return c.execute('SELECT * FROM games WHERE name=?', (game,)).fetchone()

def getPeriod(connection, period):
    c = connection.cursor()
    return c.execute('SELECT * FROM types WHERE period=?', (period,)).fetchone()

def getCurrentCompilationVideoCount(connection, channel_id, game_id, type_id):
    """
        Get number to use in video title. (Count of items + 1)
    """
    c = connection.cursor()

    t = (channel_id, game_id, type_id) # Example: FortniteHighlights, Fortnite, Day (1, 5, 1)
    last_video = c.execute('SELECT COUNT(*) FROM videos WHERE channel_id=? AND game_id=? AND type_id=? ORDER BY id DESC', t).fetchone()
    
    if last_video:
        return last_video[0] + 1
    else:
        return 1

def insertVideo(connection, title, date, type_id, game_id, channel_id):
    c = connection.cursor()
    c.execute("insert into videos (title, date, type_id, game_id, channel_id) values (?, ?, ?, ?, ?)", (title, date, type_id, game_id, channel_id))
    connection.commit()

def closeConnection(connection):
    connection.close()
