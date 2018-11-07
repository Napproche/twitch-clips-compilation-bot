from models.database import Database

if __name__ == "__main__":
    """
        Run this script to create the SQLite database.
        The database is needed for the bot to work properly.
    """
    database = Database()
    database.create_database()
    database.close_connection()    
