import sqlite3
import constants


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(constants.DATABASE_LOCATION)

    def get_destination(self, destination):
        """
            Checks if a destination exists. If it does, it will return the information.
            If it doesn't exist, it will create a new destination and return this record.
        """
        instance = self.does_destination_exist(destination)
        if instance:
            return instance
        else:
            return self.create_destination(destination)

    def does_destination_exist(self, destination):
        """
            Return True if the destination already exists, False if not.
        """
        c = self.connection.cursor()
        destination = c.execute(
            'SELECT * FROM destinations WHERE name=?', (destination,)).fetchone()
        return destination if destination else None

    def create_destination(self, destination):
        """
            Create a new destination.
        """
        c = self.connection.cursor()
        c.execute("insert into destinations (name) values (?)", (destination, ))
        destination = c.execute(
            'SELECT * FROM destinations WHERE name=?', (destination,)).fetchone()
        self.connection.commit()
        return destination

    def get_channel(self, name, slug, logo, url):
        c = self.connection.cursor()
        channel = c.execute('SELECT * FROM channels WHERE slug=?', (slug,)).fetchone()
        if channel:
            return channel
        else:
            c.execute("insert into channels (name, slug, logo, url) values (?, ?, ?, ?)", (name, slug, logo, url))
            channel = c.execute('SELECT * FROM channels WHERE slug=?', (slug,)).fetchone()
            self.connection.commit()
            return channel

    def get_game(self, game):
        c = self.connection.cursor()
        return c.execute('SELECT * FROM games WHERE name=?', (game,)).fetchone()

    def get_video_type(self, video_type):
        c = self.connection.cursor()
        return c.execute('SELECT * FROM types WHERE type=?', (video_type,)).fetchone()

    def get_current_compilation_video_count(self, destination_id, game_id, type_id):
        """
            Get number to use in video title. (Count of items + 1)
        """
        c = self.connection.cursor()

        # Example: FortniteHighlights, Fortnite, Day (1, 5, 1)
        t = (destination_id, game_id, type_id)
        last_video = c.execute(
            'SELECT COUNT(*) FROM videos WHERE destination_id=? AND game_id=? AND type_id=? ORDER BY id DESC', t).fetchone()

        if last_video:
            return last_video[0] + 1
        else:
            return 1

    def insert_video(self, title, date, type_id, game_id, destination_id):
        c = self.connection.cursor()
        c.execute("insert into videos (title, date, type_id, game_id, destination_id) values (?, ?, ?, ?, ?)",
                  (title, date, type_id, game_id, destination_id))
        self.connection.commit()
        return c.lastrowid

    def insert_clip(self, title, slug, views, date, channel_id, game_id):
        clip = self.does_clip_exist(slug)
        if clip:
            return clip[0]
        else:  
            c = self.connection.cursor()
            c.execute("insert into clips (title, slug, views, date, channel_id, game_id) values (?, ?, ?, ?, ?, ?)",
                    (title, slug, views, date, channel_id, game_id))
            self.connection.commit()
            return c.lastrowid

    def does_clip_exist(self, slug):
        c = self.connection.cursor()
        clip = c.execute('SELECT * FROM clips WHERE slug=?', (slug,)).fetchone()
        return clip if clip else None

    def insert_videos_clips(self, video_id, clip_id):
        c = self.connection.cursor()
        c.execute("insert into videos_clips (video_id, clip_id) values (?, ?)", (video_id, clip_id))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def create_database(self):
        """
            Create the database.
        """
        c = self.connection.cursor()

        c.execute('''
            CREATE TABLE types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT
            )''')

        c.execute('''
            CREATE TABLE games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                full TEXT
            )''')

        c.execute('''
            CREATE TABLE destinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )''')

        c.execute('''
            CREATE TABLE channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                slug TEXT,
                logo TEXT,
                url TEXT
            )''')

        c.execute('''
            CREATE TABLE clips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                slug TEXT,
                views INTEGER,
                date TEXT,
                channel_id INTEGER,
                game_id INTEGER,
                FOREIGN KEY(channel_id) REFERENCES channels(id),
                FOREIGN KEY(game_id) REFERENCES games(id)
            )''')

        c.execute('''
            CREATE TABLE videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date TEXT,
                type_id INTEGER,
                game_id INTEGER,
                destination_id INTEGER,
                FOREIGN KEY(type_id) REFERENCES types(id),
                FOREIGN KEY(game_id) REFERENCES games(id),
                FOREIGN KEY(destination_id) REFERENCES destinations(id)
            )''')

        c.execute('''
            CREATE TABLE videos_clips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                clip_id INTEGER,
                FOREIGN KEY(video_id) REFERENCES videos(id),
                FOREIGN KEY(clip_id) REFERENCES clips(id)
            )''')

        c.execute("INSERT INTO types VALUES (1, 'day')")
        c.execute("INSERT INTO types VALUES (2, 'week')")
        c.execute("INSERT INTO types VALUES (3, 'month')")
        c.execute("INSERT INTO types VALUES (4, 'compilation')")

        c.execute("INSERT INTO games VALUES (1, 'Fortnite', 'Fortnite')")

        self.connection.commit()
