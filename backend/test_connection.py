import pyodbc
import time

start = time.time()

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=OBSERVATOIRE_STAGIAIRE;"
    "UID=sa;"
    "PWD=;"
)

print("Temps :", time.time() - start)

conn.close()