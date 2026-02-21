import pandas as pd
import numpy as np
import os

print("WORKDIR:", os.getcwd())


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
dim_date.to_csv("dim_date.csv", index=False)

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
dim_beer.to_csv("dim_beer.csv", index=False)

# ---------------- DIM_CUSTOMER ----------------
dim_customer = pd.DataFrame({
    "customer_id": range(1,11),
    "customer_name": [f"Customer_{i}" for i in range(1,11)],
    "channel": np.random.choice(["Retail","HoReCa","Wholesale","Online"], 10),
    "region": np.random.choice(["South","North","East","West"], 10),
    "size": np.random.choice(["Small","Medium","Large"], 10)
})
dim_customer.to_csv("dim_customer.csv", index=False)

# ---------------- DIM_PLANT ----------------
dim_plant = pd.DataFrame({
    "plant": ["Bielsko","Katowice","Warszawa"],
    "city": ["Bielsko","Katowice","Warszawa"],
    "capacity_l": [500000,400000,600000],
    "opened_year": [2000,2005,2010]
})
dim_plant.to_csv("dim_plant.csv", index=False)

# ---------------- DIM_DEFECT ----------------
dim_defect = pd.DataFrame({
    "defect_type": ["Infection","Flat taste","Overcarbonation","Cloudy","Oxidation"],
    "description": ["Microbial contamination","Lack of flavor","Too much CO2","Hazy beer","Oxidized flavor"],
    "criticality": ["High","Medium","Medium","Low","High"]
})
dim_defect.to_csv("dim_defect.csv", index=False)
rows = []
for date in dim_date['date']:
    season_multiplier = 1.2 if date.month in [6,7,8] else 1.0
    for plant in dim_plant['plant']:
        for line in ["L1","L2","L3","L4"]:
            for beer_id in dim_beer['beer_id']:
                base_volume = np.random.randint(800,1200)
                planned_volume = int(base_volume * np.random.uniform(0.9,1.1) * season_multiplier)
                # Waste
                new_beers = [4,5]
                base_waste_pct = np.random.uniform(0.01,0.05)
                if beer_id in new_beers:
                    base_waste_pct *= 1.05
                waste = int(planned_volume * base_waste_pct)
                produced = planned_volume - waste
                downtime = np.random.randint(0,121)
                if np.random.rand() < 0.05:
                    downtime = np.random.randint(81,121)
                shift = np.random.choice(["A","B","C"])
                batch_id = f"{date.strftime('%Y%m%d')}_{line}_{beer_id}"
                rows.append([
                    date, plant, line, beer_id, batch_id,
                    planned_volume, produced, waste, downtime, shift
                ])
df_production = pd.DataFrame(rows, columns=[
    "date","plant","brew_line","beer_id","batch_id",
    "planned_volume_l","produced_volume_l","waste_l","downtime_min","shift"
])
df_production.to_csv("fact_production.csv", index=False)
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
df_quality.to_csv("fact_quality.csv", index=False)
sales_rows = []
for date in dim_date['date']:
    for beer_id in dim_beer['beer_id']:
        for customer_id in dim_customer['customer_id']:
            # sezonowość
            season_multiplier = 1.3 if date.month in [6,7,8] else 1.0
            qty = int(np.random.randint(50,200) * season_multiplier)
            price = dim_beer.loc[dim_beer['beer_id']==beer_id,'base_price'].values[0]
            discount = np.random.uniform(0,0.15)
            revenue = qty * price * (1-discount)
            channel = dim_customer.loc[dim_customer['customer_id']==customer_id,'channel'].values[0]
            region = dim_customer.loc[dim_customer['customer_id']==customer_id,'region'].values[0]
            sales_rows.append([date, customer_id, beer_id, channel, qty, revenue, discount, region])
df_sales = pd.DataFrame(sales_rows, columns=[
    "date","customer_id","beer_id","channel","qty_l","revenue","discount","region"
])
df_sales.to_csv("fact_sales.csv", index=False)
cost_types = ["Malt","Hops","Energy","Labor","Transport","Maintenance","Marketing"]
cost_rows = []
for date in dim_date.drop_duplicates(subset='month')['date']:
    for plant in dim_plant['plant']:
        for cost in cost_types:
            base_cost = np.random.randint(1000,5000)
            # losowy trend
            if cost=="Energy" and date.year==2024:
                base_cost *= 1.25
            cost_rows.append([date, plant, cost, base_cost])
df_costs = pd.DataFrame(cost_rows, columns=["date","plant","cost_type","amount"])
df_costs.to_csv("fact_costs.csv", index=False)
inventory_rows = []
for date in dim_date['date']:
    for beer_id in dim_beer['beer_id']:
        for plant in dim_plant['plant']:
            stock = np.random.randint(100,1000)
            expiry_date = date + pd.Timedelta(days=90)
            status = "Expired" if date > expiry_date else "OK"
            inventory_rows.append([date, beer_id, plant, stock, expiry_date, status])
df_inventory = pd.DataFrame(inventory_rows, columns=[
    "date","beer_id","location","stock_l","expiry_date","status"
])
df_inventory.to_csv("fact_inventory.csv", index=False)
