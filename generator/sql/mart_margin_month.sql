CREATE OR REPLACE VIEW mart_margin_month AS
WITH costs AS (
    SELECT
        EXTRACT(year FROM date) AS year,
        EXTRACT(month FROM date) AS month,
        plant,
        beer_id,
        SUM(batch_cost) AS cogs
    FROM fact_production
    GROUP BY 1,2,3,4
),

opex_costs AS (
    SELECT
        EXTRACT(year FROM date) AS year,
        EXTRACT(month FROM date) AS month,
        plant,
        SUM(amount) AS opex
    FROM fact_costs
    GROUP BY 1,2,3
),

sales_data AS (
    SELECT
        EXTRACT(year FROM s.date) AS year,
        EXTRACT(month FROM s.date) AS month,
        plant,
        beer_id,
        SUM(s.revenue) AS revenue
    FROM fact_sales s
    GROUP BY 1,2,3,4


),

plant_revenue AS (
    SELECT
        year,
        month,
        plant,
        SUM(revenue) AS total_revenue_plant
    FROM sales_data
    GROUP BY 1,2,3
),

combined AS (
    SELECT
        s.year,
        s.month,
        s.plant,
        s.beer_id,
        s.revenue,
        COALESCE(c.cogs,0) AS cogs,
    FROM sales_data s
    LEFT JOIN costs c
        ON s.year = c.year
        AND s.month = c.month
        AND s.plant = c.plant
        AND s.beer_id = c.beer_id
),

base AS (
    SELECT
        year,
        month,
        MAKE_DATE(year, month, 1) AS month_date,
        plant,
        beer_id,
        revenue,
        cogs AS total_cost,
        revenue - cogs AS margin
    FROM combined
),

with_yoy AS (
    SELECT
        cur.*,
        prev.margin AS margin_ly
    FROM base cur
    LEFT JOIN base prev
        ON cur.plant = prev.plant
        AND cur.beer_id = prev.beer_id
        AND cur.year = prev.year + 1
        AND cur.month = prev.month
)

SELECT
    *,
    CASE
        WHEN margin_ly IS NOT NULL AND margin_ly <> 0
            THEN (margin - margin_ly) / ABS(margin_ly)
        WHEN margin_ly = 0 AND margin > 0
            THEN 1
        ELSE NULL
    END AS yoy_margin_pct
FROM with_yoy;
