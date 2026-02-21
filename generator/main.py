import pandas as pd
import numpy as np
import duckdb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("WORKDIR:", os.getcwd())
np.random.seed(42)


# ---------------- DIM_DATE ----------------
dates = pd.date_range("2023-01-01", "2025-12-31")
dim_date = pd.DataFrame({
    "date": dates,
    "year": dates.year,
    "quarter": dates.quarter,
    "month": dates.month,
    "week": dates.isocalendar().week,
    "season": np.where(dates.month.isin([12,1,2]), "Winter",
              np.where(dates.month.isin([3,4,5]), "Spring",
              np.where(dates.month.isin([6,7,8]), "Summer", "Autumn")))
})


# ---------------- DIM_BEER ----------------
dim_beer = pd.DataFrame({
    "beer_id": [1,2,3,4,5],
    "beer_name": ["Lager","IPA","Stout","Pils","Wheat"],
    "style": ["Lager","IPA","Stout","Pils","Wheat"],
    "abv": [5.0,6.2,7.0,4.8,5.5],
    "ibu": [20,50,40,25,18],
    "launch_date": pd.to_datetime(["2023-01-01","2023-03-01","2023-06-01","2024-01-01","2024-03-01"]),
    "base_price": [10,12,14,11,9]
})

launch_dict = dim_beer.set_index("beer_id")["launch_date"].to_dict()


# ---------------- DIM_COST_PROFILE ----------------

dim_cost = pd.DataFrame({
    "beer_id": dim_beer["beer_id"],
    "material_cost_l": np.random.uniform(1.5, 3.0, len(dim_beer)),
    "energy_cost_l": np.random.uniform(0.3, 0.8, len(dim_beer)),
    "labor_cost_l": np.random.uniform(0.2, 0.6, len(dim_beer))
})




# ---------------- DIM_CUSTOMER ----------------
dim_customer = pd.DataFrame({
    "customer_id": range(1,11),
    "customer_name": [f"Customer_{i}" for i in range(1,11)],
    "channel": np.random.choice(["Retail","HoReCa","Wholesale","Online"], 10),
    "region": np.random.choice(["South","North","East","West"], 10),
    "size": np.random.choice(["Small","Medium","Large"], 10)
})


# ---------------- DIM_PLANT ----------------
dim_plant = pd.DataFrame({
    "plant": ["Bielsko","Katowice","Warszawa"],
    "city": ["Bielsko","Katowice","Warszawa"],
    "capacity_l": [500000,400000,600000],
    "opened_year": [2000,2005,2010]
})


# ---------------- DIM_DEFECT ----------------
dim_defect = pd.DataFrame({
    "defect_type": ["Infection","Flat taste","Overcarbonation","Cloudy","Oxidation"],
    "description": ["Microbial contamination","Lack of flavor","Too much CO2","Hazy beer","Oxidized flavor"],
    "criticality": ["High","Medium","Medium","Low","High"]
})

lines = []
# ---------------- DIM_LINE ----------------
line_id = 1
for plant in dim_plant["plant"]:
    for line in ["L1","L2","L3","L4"]:
        lines.append([line_id, plant, line])
        line_id += 1

dim_line = pd.DataFrame(lines, columns=["line_id","plant","line_code"])
line_lookup = dim_line.set_index(["plant", "line_code"])["line_id"].to_dict()

# ---------------- TARGET STOCK LEVELS ----------------
target_stock = {
    "Bielsko": 80000,
    "Katowice": 100000,
    "Warszawa": 120000
}

# ---------------- fact_production ----------------


plant_profiles = {
    "Bielsko": {
        "volume_mult": 0.9,
        "waste_mult": 1.2,
        "labor_mult": 0.8,
        "downtime_mult": 1.3
    },
    "Katowice": {
        "volume_mult": 1.0,
        "waste_mult": 1.0,
        "labor_mult": 1.0,
        "downtime_mult": 1.0
    },
    "Warszawa": {
        "volume_mult": 1.15,
        "waste_mult": 0.8,
        "labor_mult": 1.3,
        "downtime_mult": 0.7
    }
}

cost_profile = dim_cost.set_index("beer_id")
rows = []

for date in dim_date['date']:
    season_multiplier = 1.2 if date.month in [6,7,8] else 1.0

    energy_multiplier = 1.25 if date.year == 2024 else 1.0
    if date.month in [12,1,2]:
        energy_multiplier *= 1.15

    for plant in dim_plant['plant']:
        for line in ["L1","L2","L3","L4"]:
            line_id = line_lookup[(plant, line)]
            for beer_id in dim_beer['beer_id']:
                beer_launch = launch_dict[beer_id]
                production_start = beer_launch - pd.Timedelta(days=14)
                if date < production_start:
                    continue
                days_from_prod_start = (date - production_start).days

                if date < beer_launch:
                    if days_from_prod_start < 14:
                        prod_ramp = days_from_prod_start / 14
                    else:
                        prod_ramp = 0.6
                else:
                    prod_ramp = 1

                       
                profile = plant_profiles[plant]

                base_volume = int(
                    np.random.randint(800,1200)
                    *profile["volume_mult"]
)

                planned_volume = int(
                     base_volume
                        * np.random.uniform(0.9,1.1)
                        * season_multiplier
                        * prod_ramp
)


                base_waste_pct = (
                    np.random.uniform(0.01,0.05)
                    * profile["waste_mult"]
)


                if beer_id in [4,5]:
                    base_waste_pct *= 1.05

                waste = int(planned_volume * base_waste_pct)
                produced = planned_volume - waste

                downtime = int(
                    np.random.randint(0,121)
                    * profile["downtime_mult"]
)


                shift = np.random.choice(["A","B","C"])
                planned_runtime_min = 24 * 60
                runtime_min = planned_runtime_min - downtime
                runtime_min = max(runtime_min, 0)

                batch_id = f"{date.strftime('%Y%m%d')}_{plant}_{line}_{beer_id}"

                # ---- COSTS ----
                mat = cost_profile.loc[beer_id, "material_cost_l"]
                eng = cost_profile.loc[beer_id, "energy_cost_l"] * energy_multiplier
                lab = cost_profile.loc[beer_id, "labor_cost_l"] * profile["labor_mult"]


                cost_per_l = mat + eng + lab

                batch_cost = produced * cost_per_l

                rows.append([
                    date,
                    plant,
                    line_id,
                    beer_id,
                    batch_id,
                    planned_volume,
                    produced,
                    waste,
                    downtime,
                    runtime_min,
                    planned_runtime_min,
                    shift,
                    cost_per_l,
                    batch_cost
])


df_production = pd.DataFrame(rows, columns=[
    "date",
    "plant",
    "line_id",
    "beer_id",
    "batch_id",
    "planned_volume_l",
    "produced_volume_l",
    "waste_l",
    "downtime_min",
    "runtime_min",
    "planned_runtime_min",
    "shift",
    "cost_per_l",
    "batch_cost"
])



# ---------------- DIM_BATCH ----------------

batch_dim = (
    df_production
    .sort_values("date")
    .groupby("batch_id", as_index=False)
    .agg(
        production_date=("date", "min"),
        beer_id=("beer_id", "first"),
        plant=("plant", "first"),
        line_id=("line_id", "first")
    )
)

# shelf life = 90 dni
batch_dim["shelf_life_days"] = 90

# expiry = produkcja + shelf life
batch_dim["expiry_date"] = (
    batch_dim["production_date"] +
    pd.to_timedelta(batch_dim["shelf_life_days"], unit="D")
)



# ---------------- fact_quality ----------------

quality_rows = []
for idx, row in df_production.iterrows():
    batch_id = row['batch_id']
    beer_id = row['beer_id']
    date = row['date']
    # losowo generujemy defekty
    if np.random.rand() < 0.2:  # 20% partii ma defekty
        num_defects = np.random.randint(1,3)
        for _ in range(num_defects):
            defect_type = np.random.choice(dim_defect['defect_type'])
            defect_qty = np.random.randint(1,50)
            severity = np.random.choice(["Low","Medium","High"])
            root_cause = np.random.choice(["Operator","Equipment","Raw material"])
            action = np.random.choice(["Rework","Discard","Adjust process"])
            quality_rows.append([date,batch_id,beer_id,defect_type,defect_qty,severity,root_cause,action])

df_quality = pd.DataFrame(quality_rows, columns=[
    "date","batch_id","beer_id","defect_type","defect_qty","severity","root_cause","action"
])


# ---------------- FACT_SALES (FROM PRODUCTION) ----------------

sales_rows = []

for idx, row in df_production.iterrows():

    batch_id = row["batch_id"]
    date = row["date"]
    beer_id = row["beer_id"]
    plant = row["plant"]
    
    produced_qty = row["produced_volume_l"]
    beer_launch = launch_dict[beer_id]

    if date < beer_launch:
     continue

    # KOREKTA 1: Sprzedaż jako funkcja produkcji
    days_since_launch = (date - beer_launch).days

    if days_since_launch < 90:
        ramp_factor = days_since_launch / 90
    else:
        ramp_factor = 1

    base_ratio = np.random.normal(0.9, 0.05)
    base_ratio = np.clip(base_ratio, 0.75, 0.98)

    sell_ratio = base_ratio * ramp_factor

    
    sellable = int(produced_qty * sell_ratio)

    customers = np.random.choice(
        dim_customer["customer_id"],
        size=np.random.randint(2,5),
        replace=False
    )

    remaining = sellable

    for cust in customers:

        if remaining <= 0:
            break

        qty = np.random.randint(
            int(remaining*0.2),
            int(remaining*0.5)+1
        )

        qty = min(qty, remaining)
        remaining -= qty

        price = dim_beer.loc[
            dim_beer["beer_id"]==beer_id,
            "base_price"
        ].values[0]

        discount = np.random.uniform(0,0.15)

        revenue = qty * price * (1-discount)

        channel = dim_customer.loc[
            dim_customer["customer_id"]==cust,
            "channel"
        ].values[0]

        region = dim_customer.loc[
            dim_customer["customer_id"]==cust,
            "region"
        ].values[0]

        sales_rows.append([
            date,
            batch_id,
            plant,
            cust,
            beer_id,
            channel,
            qty,
            revenue,
            discount,
            region
        ])


df_sales = pd.DataFrame(
    sales_rows,
    columns=[
        "date",
        "batch_id",
        "plant",
        "customer_id",
        "beer_id",
        "channel",
        "qty_l",
        "revenue",
        "discount",
        "region"
    ]
)



# ---------------- FACT_costs  ----------------
# Definicja mnożników bazowych dla realizmu
cost_profiles = {
    "Malt": 8000, 
    "Hops": 3000, 
    "Energy": 5000, 
    "Labor": 12000, 
    "Transport": 4000, 
    "Maintenance": 2000, 
    "Marketing": 6000
}

cost_rows = []
month_dates = (
    dim_date
    .assign(year_month=dim_date['date'].dt.to_period('M'))
    .drop_duplicates(subset='year_month')
)

for date in month_dates['date']:
    for plant in dim_plant['plant']:
        for cost, base_val in cost_profiles.items():
            # Fluktuacja +/- 10% od bazy
            variation = np.random.uniform(0.9, 1.1)
            final_cost = base_val * variation
            
            # Warunek dla Energy w 2024 - wzrost o 25%
            if cost == "Energy" and date.year == 2024:
                final_cost *= 1.25
            
            # Dodanie inflacji (np. koszty rosną o 5% z każdym rokiem)
            years_diff = date.year - dim_date['date'].dt.year.min()
            final_cost *= (1.05 ** years_diff)
            
            cost_rows.append([date, plant, cost, round(final_cost, 2)])

df_costs = pd.DataFrame(cost_rows, columns=["date", "plant", "cost_type", "amount"])


# ---------------- FACT_INVENTORY (PLANT + BEER DAILY) ----------------

inventory_rows = []

# Produkcja dzienna
prod_daily = (
    df_production
    .groupby(["date", "plant", "beer_id"])["produced_volume_l"]
    .sum()
    .reset_index()
)

# Sprzedaż dzienna
sales_daily = (
    df_sales
    .groupby(["date", "plant", "beer_id"])["qty_l"]
    .sum()
    .reset_index()
)


# >>> SŁOWNIKI TWORZYMY RAZ <<<
prod_dict = {
    (r.date, r.plant, r.beer_id): r.produced_volume_l
    for r in prod_daily.itertuples()
}

sales_dict = {
    (r.date, r.plant, r.beer_id): r.qty_l
    for r in sales_daily.itertuples()
}


# ---------------- STARTOWY STOCK ----------------

current_stock = {}

for plant in dim_plant["plant"]:
    for beer in dim_beer["beer_id"]:

        launch_date = launch_dict[beer]

        # Tylko piwa istniejące od 2023-01-01 dostają startowy stock
        if launch_date == pd.Timestamp("2023-01-01"):
            current_stock[(plant, beer)] = np.random.randint(2000, 5000)
        else:
            current_stock[(plant, beer)] = 0



# Symulacja dzień po dniu
for date in dim_date["date"]:

    for plant in dim_plant["plant"]:
        for beer in dim_beer["beer_id"]:
            launch_date = launch_dict[beer]
            production_start = launch_date - pd.Timedelta(days=14)

            if date < production_start:
                continue

            key = (plant, beer)

            stock_yesterday = current_stock.get(key, 0)

            # KOREKTA 3: Ograniczenie produkcji przy overstock
            prod_today_raw = prod_dict.get((date, plant, beer), 0)
            if stock_yesterday > target_stock[plant]:
                prod_today = int(prod_today_raw * 0.5)  # redukcja produkcji o 50%
            else:
                prod_today = prod_today_raw

            # Sprzedaż dziś
            sold_today = sales_dict.get((date, plant, beer), 0)

            # Nowy stan
            stock_today = stock_yesterday + prod_today - sold_today
            stock_today = max(stock_today, 0)

            # Status
            if stock_today == 0:
                status = "Stockout"
            elif stock_today < 1000:
                status = "Low stock"
            elif stock_today > target_stock[plant] * 1.2:  # 20% powyżej targetu
                status = "Overstock"
            else:
                status = "OK"

            inventory_rows.append([
                date,
                plant,
                beer,
                stock_today,
                status
            ])

            current_stock[key] = stock_today


df_inventory = pd.DataFrame(
    inventory_rows,
    columns=[
        "date",
        "plant",
        "beer_id",
        "stock_l",
        "status"
    ]
)




# ---------------- zapis do bazy ----------------
db_path = os.path.join("..", "database", "brewery.duckdb")
con = duckdb.connect(db_path)

con.execute("CREATE OR REPLACE TABLE fact_sales AS SELECT * FROM df_sales")
con.execute("CREATE OR REPLACE TABLE fact_production AS SELECT * FROM df_production")
con.execute("CREATE OR REPLACE TABLE fact_inventory AS SELECT * FROM df_inventory")
con.execute("CREATE OR REPLACE TABLE dim_beer AS SELECT * FROM dim_beer")
con.execute("CREATE OR REPLACE TABLE dim_plant AS SELECT * FROM dim_plant")
con.execute("CREATE OR REPLACE TABLE dim_date AS SELECT * FROM dim_date")
con.execute("CREATE OR REPLACE TABLE dim_customer AS SELECT * FROM dim_customer")
con.execute("CREATE OR REPLACE TABLE dim_cost_profile AS SELECT * FROM dim_cost")
con.execute("CREATE OR REPLACE TABLE dim_defect AS SELECT * FROM dim_defect")
con.execute("CREATE OR REPLACE TABLE dim_batch AS SELECT * FROM batch_dim")
con.execute("CREATE OR REPLACE TABLE fact_quality AS SELECT * FROM df_quality")
con.execute("CREATE OR REPLACE TABLE fact_costs AS SELECT * FROM df_costs")
con.execute("CREATE OR REPLACE TABLE dim_line AS SELECT * FROM dim_line")


con.close()
con = duckdb.connect(db_path)

df_preview = con.execute("""
    SELECT plant, beer_id, SUM(stock_l) AS total_stock
    FROM fact_inventory
    WHERE date = (SELECT MAX(date) FROM fact_inventory)
    GROUP BY plant, beer_id
    ORDER BY total_stock DESC
""").df()

df_preview


# =========================
# Tworzenie martów / widoków
# =========================

sql_dir = os.path.join(BASE_DIR, "sql")

for file in sorted(os.listdir(sql_dir)):
    if file.endswith(".sql"):
        sql_path = os.path.join(sql_dir, file)
        
        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()
            con.execute(sql)
        
        print(f"✅ Wykonano {file}")


# ---------------- SANITY CHECK (KOREKTA 5) ----------------
print("\n" + "="*50)
print("SANITY CHECK - Spójność danych")
print("="*50)

total_produced = df_production["produced_volume_l"].sum()
total_sales = df_sales["qty_l"].sum()
latest_date = df_inventory["date"].max()
latest_stock = df_inventory[df_inventory["date"] == latest_date]["stock_l"].sum()

print(f"Całkowita produkcja: {total_produced:,.0f} L")
print(f"Całkowita sprzedaż:  {total_sales:,.0f} L")
print(f"Stan na koniec ({latest_date.date()}): {latest_stock:,.0f} L")
print(f"Różnica (Prod - Sales - Stock): {total_produced - total_sales - latest_stock:,.0f} L")

# Weryfikacja
   
print(f"\nStosunek sprzedaży do produkcji: {total_sales/total_produced:.2%}")
print("="*50)