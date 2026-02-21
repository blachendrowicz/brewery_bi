import os
import duckdb

# Ścieżka bazowa folderu generator
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ścieżka do SQL
sql_path = os.path.join(BASE_DIR, "sql", "mart_margin_month.sql")

# Ścieżka do bazy
db_path = os.path.join(BASE_DIR, "..", "database", "brewery.duckdb")

# Połączenie
conn = duckdb.connect(db_path)

# Wykonanie SQL
with open(sql_path, "r", encoding="utf-8") as f:
    sql = f.read()
    conn.execute(sql)

print("✅ mart_margin_monthy utworzony")

# Szybki test
test_query = """
SELECT *
FROM mart_margin_month
ORDER BY month
LIMIT 10
"""

wynik = conn.execute(test_query).fetchdf()

print("\n📊 Podgląd danych:")
print(wynik.to_string(index=False))

conn.close()
