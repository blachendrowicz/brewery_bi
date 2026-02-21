import os
import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sql_path = os.path.join(BASE_DIR, "sql", "create_dimdate_view.sql")
db_path = os.path.join(BASE_DIR, "..", "database", "brewery.duckdb")

conn = duckdb.connect(db_path)

with open(sql_path, "r") as f:
    sql = f.read()
    conn.execute(sql)

print("✅ Widok utworzony")

# Sprawdzenie
wynik = conn.execute("""
    SELECT 
        date,
        Day_of_Week,
        year_month,
        Qtr_Year
    FROM dim_date_sql
    WHERE date BETWEEN '2024-01-01' AND '2024-01-07'
    ORDER BY date
""").fetchdf()

print("\n📊 Dane z widoku:")
print(wynik.to_string(index=False))

conn.close()