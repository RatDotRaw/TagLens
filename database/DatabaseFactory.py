from .neo4j.neo4j_db import Neo4jIntegration
from .sqlite.sqlite_db import SqliteIntegration

class DatabaseFactory():

    @staticmethod
    def create_database(db_type):
        """
        Creates and returns an instance of the specified database integration.
        
        Args:
        - db_type (str): The type of database to create. Supported types are 'sqlite' and 'neo4j'.
        
        Returns:
        - DatabaseIntegration: An instance of the requested database integration class.
        
        Raises:
        - ValueError: If an unsupported database type is provided.
        """
        if db_type == 'sqlite':
            return SqliteIntegration()
        elif db_type == 'neo4j':
            return Neo4jIntegration()
        else:
            raise ValueError("Unsupported database type: {}".format(db_type))