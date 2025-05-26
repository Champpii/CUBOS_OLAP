from src.conections.db_conection import Connection

try:
    connection = Connection()
    print("URI de conexión:", connection.connect())
    print("Conexión a SQL Server exitosa.")
except Exception as e:
    print(f"Error al conectar a SQL Server: {e}")
