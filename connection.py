import os
import mysql.connector
import dotenv

dotenv.load_dotenv()

conexaoBanco = mysql.connector.connect(
   host = os.getenv("DATABASE_HOST"),
   user = os.getenv("DATABASE_USER"),
   password = os.getenv("DATABASE_PASS"),
   database = os.getenv("DATABASE_DB"),
   port = os.getenv("DATABASE_PORT")
)