SELECT * from dim_date; 

SELECT
    d.scheme_name,
    a.aum_crore
FROM fact_aum a
JOIN dim_fund d
    ON a.amfi_code = d.amfi_code
ORDER BY a.aum_crore DESC
LIMIT 5;

SELECT
strftime('%Y-%m', n.date_key) AS month,
ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
GROUP BY strftime('%Y-%m', n.date_key)
ORDER BY month;

WITH yearly_sip AS (
    SELECT
        strftime('%Y', transaction_date) AS year,
        SUM(amount_inr) AS total_sip_amount
    FROM fact_transactions
    WHERE UPPER(transaction_type) = 'SIP'
    GROUP BY strftime('%Y', transaction_date)
)

SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE UPPER(transaction_type) = 'SIP'
GROUP BY strftime('%Y', transaction_date)
ORDER BY year;

SELECT
    d.scheme_name,
    d.fund_house,
    d.category,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct ASC;

SELECT
    d.scheme_name,
    d.fund_house,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
ORDER BY p.return_5yr_pct DESC
LIMIT 5;

SELECT
    d.fund_house,
    ROUND(AVG(a.aum_crore), 2) AS avg_aum
FROM fact_aum a
JOIN dim_fund d
    ON a.amfi_code = d.amfi_code
GROUP BY d.fund_house
ORDER BY avg_aum DESC;	

SELECT
    payment_mode,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY payment_mode
ORDER BY total_amount DESC;

SELECT
    city_tier,
    ROUND(AVG(amount_inr), 2) AS avg_investment,
    COUNT(*) AS transactions
FROM fact_transactions
GROUP BY city_tier
ORDER BY avg_investment DESC;

SELECT
    d.scheme_name,
    p.risk_grade,
    ROUND(p.return_5yr_pct, 2) AS return_5yr_pct,
    ROUND(p.sharpe_ratio, 2) AS sharpe_ratio
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
ORDER BY p.return_5yr_pct DESC;