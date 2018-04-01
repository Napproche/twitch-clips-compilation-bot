from services import database as databaseService

if __name__ == "__main__":
    """
        Run this script to create the SQLite database.
        The database is needed for the bot to work properly.
    """
    connection = databaseService.getDatabaseConnection()
    databaseService.initializeDatabaseTables(connection)
    databaseService.closeConnection(connection)
