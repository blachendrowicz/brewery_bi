-- Tworzenie widoku rozszerzającego tabelę dimdate
-- Dni tygodnia w formacie ISO (poniedziałek=1, niedziela=7)

CREATE OR REPLACE VIEW dim_date_sql AS
SELECT 
    *,  -- wszystkie oryginalne kolumny
    
    -- ISO day of week (1-7, poniedziałek=1)
    EXTRACT(ISODOW FROM date) AS Day_of_Week,
    
    -- year_month (YYYY-MM)
    STRFTIME(date, '%Y-%m') AS year_month,
    
    -- Qtr_Year (YYYY-QX)
    STRFTIME(date, '%Y') || '-Q' || EXTRACT(QUARTER FROM date) AS Qtr_Year
    
    
FROM dim_date;