import os
from sqlalchemy.exc import SQLAlchemyError

class Connection:
    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.database = os.environ.get('DB_NAME')
        self.port = os.environ.get('DB_PORT')

    def connect(self):
        try:
            return f"mssql+pyodbc://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
        except SQLAlchemyError as e:
            print(f"Error al construir la conexión: {e}")
