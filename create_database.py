from services import database as databaseService

if __name__ == "__main__":
    connection = databaseService.getDatabaseConnection()
    databaseService.initializeDatabaseTables(connection)
    databaseService.closeConnection(connection)
