-- ETL Testing SQL Examples
-- Collection of reusable SQL queries for ETL validation

-- ============================================
-- EXTRACT PHASE TESTING
-- ============================================

-- 1. Source Data Availability Check
SELECT 
    'Source Data Availability' as test_name,
    COUNT(*) as record_count,
    MIN(load_date) as earliest_date,
    MAX(load_date) as latest_date,
    MAX(last_updated) as last_update_time,
    CURRENT_TIMESTAMP - MAX(last_updated) as data_age_hours,
    CASE 
        WHEN COUNT(*) > 0 AND CURRENT_TIMESTAMP - MAX(last_updated) < INTERVAL '24 hours' 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_status
FROM source_orders
WHERE load_date = CURRENT_DATE;

-- 2. Source Schema Validation
SELECT 
    column_name,
    data_type,
    is_nullable,
    CASE 
        WHEN column_name IN ('order_id', 'customer_id', 'order_date', 'amount') 
        THEN 'REQUIRED' 
        ELSE 'OPTIONAL' 
    END as requirement
FROM information_schema.columns
WHERE table_name = 'source_orders'
ORDER BY ordinal_position;

-- 3. Source Data Quality - Null Check
SELECT 
    'Null Check' as test_name,
    COUNT(*) as total_records,
    COUNT(order_id) as non_null_order_id,
    COUNT(customer_id) as non_null_customer_id,
    COUNT(order_date) as non_null_order_date,
    COUNT(amount) as non_null_amount,
    COUNT(*) - COUNT(order_id) as null_order_id_count,
    ROUND(100.0 * (COUNT(*) - COUNT(order_id)) / COUNT(*), 2) as null_percentage,
    CASE 
        WHEN COUNT(*) - COUNT(order_id) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM source_orders
WHERE load_date = CURRENT_DATE;

-- 4. Source Data Quality - Duplicate Check
SELECT 
    'Duplicate Check' as test_name,
    order_id,
    COUNT(*) as duplicate_count,
    'FAIL' as test_status
FROM source_orders
WHERE load_date = CURRENT_DATE
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 5. Source Data Quality - Data Range Validation
SELECT 
    'Data Range Validation' as test_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN amount < 0 THEN 1 END) as negative_amounts,
    COUNT(CASE WHEN amount > 1000000 THEN 1 END) as excessive_amounts,
    COUNT(CASE WHEN order_date < '2020-01-01' THEN 1 END) as old_dates,
    COUNT(CASE WHEN order_date > CURRENT_DATE THEN 1 END) as future_dates,
    CASE 
        WHEN COUNT(CASE WHEN amount < 0 OR amount > 1000000 OR order_date < '2020-01-01' OR order_date > CURRENT_DATE THEN 1 END) = 0 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM source_orders
WHERE load_date = CURRENT_DATE;

-- ============================================
-- TRANSFORM PHASE TESTING
-- ============================================

-- 6. Business Rule Validation - Revenue Calculation
WITH source_data AS (
    SELECT 
        order_id,
        quantity,
        unit_price,
        discount_rate,
        (quantity * unit_price * (1 - discount_rate)) as calculated_revenue
    FROM source_orders
    WHERE load_date = CURRENT_DATE
),
target_data AS (
    SELECT 
        order_id,
        revenue
    FROM target_order_summary
    WHERE load_date = CURRENT_DATE
)
SELECT 
    'Revenue Calculation' as test_name,
    s.order_id,
    s.calculated_revenue as expected_revenue,
    t.revenue as actual_revenue,
    ABS(s.calculated_revenue - t.revenue) as difference,
    CASE 
        WHEN ABS(s.calculated_revenue - t.revenue) < 0.01 THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM source_data s
JOIN target_data t ON s.order_id = t.order_id
WHERE ABS(s.calculated_revenue - t.revenue) >= 0.01;

-- 7. Aggregation Validation - Customer Summary
WITH manual_aggregation AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date
    FROM source_orders
    WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY customer_id
),
etl_aggregation AS (
    SELECT 
        customer_id,
        order_count,
        total_amount,
        avg_amount,
        first_order_date,
        last_order_date
    FROM target_customer_summary
    WHERE snapshot_date = CURRENT_DATE
)
SELECT 
    'Customer Aggregation' as test_name,
    m.customer_id,
    m.order_count as manual_count,
    e.order_count as etl_count,
    ABS(m.total_amount - e.total_amount) as amount_difference,
    CASE 
        WHEN m.order_count = e.order_count 
         AND ABS(m.total_amount - e.total_amount) < 0.01 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM manual_aggregation m
FULL OUTER JOIN etl_aggregation e ON m.customer_id = e.customer_id
WHERE m.order_count != e.order_count 
   OR ABS(m.total_amount - e.total_amount) >= 0.01;

-- 8. Join Validation - Referential Integrity
SELECT 
    'Referential Integrity' as test_name,
    o.customer_id,
    COUNT(*) as orphaned_count,
    'FAIL' as test_status
FROM target_orders o
LEFT JOIN target_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND o.load_date = CURRENT_DATE
GROUP BY o.customer_id;

-- 9. Data Type Conversion Validation
SELECT 
    'Data Type Conversion' as test_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN amount::text ~ '^[0-9]+\.?[0-9]*$' THEN 1 END) as valid_numeric,
    COUNT(CASE WHEN order_date::text ~ '^\d{4}-\d{2}-\d{2}$' THEN 1 END) as valid_date,
    CASE 
        WHEN COUNT(*) = COUNT(CASE WHEN amount::text ~ '^[0-9]+\.?[0-9]*$' THEN 1 END)
         AND COUNT(*) = COUNT(CASE WHEN order_date::text ~ '^\d{4}-\d{2}-\d{2}$' THEN 1 END)
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE;

-- ============================================
-- LOAD PHASE TESTING
-- ============================================

-- 10. Record Count Reconciliation
WITH source_count AS (
    SELECT COUNT(*) as src_count
    FROM source_orders
    WHERE load_date = CURRENT_DATE
      AND status = 'ACTIVE'  -- Apply same filters as ETL
),
target_count AS (
    SELECT COUNT(*) as tgt_count
    FROM target_orders
    WHERE load_date = CURRENT_DATE
),
filtered_count AS (
    SELECT COUNT(*) as filtered
    FROM source_orders
    WHERE load_date = CURRENT_DATE
      AND status != 'ACTIVE'
)
SELECT 
    'Record Count Reconciliation' as test_name,
    s.src_count as source_records,
    t.tgt_count as target_records,
    f.filtered as filtered_records,
    s.src_count - f.filtered as expected_target,
    ABS((s.src_count - f.filtered) - t.tgt_count) as difference,
    CASE 
        WHEN (s.src_count - f.filtered) = t.tgt_count THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM source_count s
CROSS JOIN target_count t
CROSS JOIN filtered_count f;

-- 11. Primary Key Uniqueness
SELECT 
    'Primary Key Uniqueness' as test_name,
    order_id,
    COUNT(*) as duplicate_count,
    'FAIL' as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 12. Incremental Load Validation
WITH source_changes AS (
    SELECT 
        order_id,
        amount,
        status,
        last_modified
    FROM source_orders
    WHERE last_modified >= CURRENT_DATE - INTERVAL '1 day'
),
target_current AS (
    SELECT 
        order_id,
        amount,
        status,
        last_modified
    FROM target_orders
    WHERE load_date = CURRENT_DATE
)
SELECT 
    'Incremental Load - New Records' as test_name,
    COUNT(*) as new_record_count,
    'INFO' as test_status
FROM source_changes s
LEFT JOIN target_current t ON s.order_id = t.order_id
WHERE t.order_id IS NULL

UNION ALL

SELECT 
    'Incremental Load - Updated Records' as test_name,
    COUNT(*) as updated_record_count,
    'INFO' as test_status
FROM source_changes s
JOIN target_current t ON s.order_id = t.order_id
WHERE s.amount != t.amount 
   OR s.status != t.status;

-- 13. Data Freshness Check
SELECT 
    'Data Freshness' as test_name,
    MAX(last_updated) as last_update_time,
    CURRENT_TIMESTAMP - MAX(last_updated) as data_age_hours,
    CASE 
        WHEN CURRENT_TIMESTAMP - MAX(last_updated) <= INTERVAL '1 hour' THEN 'PASS'
        WHEN CURRENT_TIMESTAMP - MAX(last_updated) <= INTERVAL '4 hours' THEN 'WARNING'
        ELSE 'FAIL'
    END as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE;

-- ============================================
-- DATA QUALITY TESTING
-- ============================================

-- 14. Completeness Check
SELECT 
    'Completeness Check' as test_name,
    COUNT(*) as total_records,
    COUNT(order_id) as order_id_complete,
    COUNT(customer_id) as customer_id_complete,
    COUNT(order_date) as order_date_complete,
    COUNT(amount) as amount_complete,
    ROUND(100.0 * COUNT(order_id) / COUNT(*), 2) as order_id_completeness_pct,
    ROUND(100.0 * COUNT(customer_id) / COUNT(*), 2) as customer_id_completeness_pct,
    CASE 
        WHEN COUNT(order_id) = COUNT(*) 
         AND COUNT(customer_id) = COUNT(*) 
         AND COUNT(order_date) = COUNT(*) 
         AND COUNT(amount) = COUNT(*)
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE;

-- 15. Accuracy Check - Value Ranges
SELECT 
    'Accuracy Check - Value Ranges' as test_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN amount < 0 THEN 1 END) as negative_amounts,
    COUNT(CASE WHEN amount > 1000000 THEN 1 END) as excessive_amounts,
    COUNT(CASE WHEN quantity < 0 THEN 1 END) as negative_quantities,
    COUNT(CASE WHEN discount_rate < 0 OR discount_rate > 1 THEN 1 END) as invalid_discounts,
    CASE 
        WHEN COUNT(CASE WHEN amount < 0 OR amount > 1000000 OR quantity < 0 OR discount_rate < 0 OR discount_rate > 1 THEN 1 END) = 0 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE;

-- 16. Consistency Check - Cross-Table Validation
WITH order_totals AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_amount
    FROM target_orders
    WHERE load_date = CURRENT_DATE
    GROUP BY customer_id
),
customer_summary AS (
    SELECT 
        customer_id,
        order_count,
        total_amount
    FROM target_customer_summary
    WHERE snapshot_date = CURRENT_DATE
)
SELECT 
    'Consistency Check' as test_name,
    o.customer_id,
    o.order_count as orders_order_count,
    c.order_count as summary_order_count,
    ABS(o.total_amount - c.total_amount) as amount_difference,
    CASE 
        WHEN o.order_count = c.order_count 
         AND ABS(o.total_amount - c.total_amount) < 0.01 
        THEN 'PASS'
        ELSE 'FAIL'
    END as test_status
FROM order_totals o
JOIN customer_summary c ON o.customer_id = c.customer_id
WHERE o.order_count != c.order_count 
   OR ABS(o.total_amount - c.total_amount) >= 0.01;

-- 17. Uniqueness Check - Business Key
SELECT 
    'Uniqueness Check - Business Key' as test_name,
    CONCAT(customer_id, '-', order_date, '-', product_id) as business_key,
    COUNT(*) as duplicate_count,
    'FAIL' as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE
GROUP BY customer_id, order_date, product_id
HAVING COUNT(*) > 1;

-- ============================================
-- PERFORMANCE TESTING
-- ============================================

-- 18. Load Performance Check
SELECT 
    'Load Performance' as test_name,
    load_date,
    COUNT(*) as records_loaded,
    MAX(load_timestamp) - MIN(load_timestamp) as load_duration,
    COUNT(*) / EXTRACT(EPOCH FROM (MAX(load_timestamp) - MIN(load_timestamp))) as records_per_second,
    CASE 
        WHEN MAX(load_timestamp) - MIN(load_timestamp) < INTERVAL '30 minutes' THEN 'PASS'
        WHEN MAX(load_timestamp) - MIN(load_timestamp) < INTERVAL '1 hour' THEN 'WARNING'
        ELSE 'FAIL'
    END as test_status
FROM target_orders
WHERE load_date = CURRENT_DATE
GROUP BY load_date;

-- ============================================
-- SUMMARY REPORT QUERY
-- ============================================

-- 19. Daily ETL Health Check Summary
SELECT 
    'Daily ETL Health Check' as report_name,
    CURRENT_DATE as check_date,
    (SELECT COUNT(*) FROM target_orders WHERE load_date = CURRENT_DATE) as total_records,
    (SELECT COUNT(DISTINCT customer_id) FROM target_orders WHERE load_date = CURRENT_DATE) as unique_customers,
    (SELECT SUM(amount) FROM target_orders WHERE load_date = CURRENT_DATE) as total_revenue,
    (SELECT MAX(last_updated) FROM target_orders WHERE load_date = CURRENT_DATE) as last_update,
    CASE 
        WHEN (SELECT COUNT(*) FROM target_orders WHERE load_date = CURRENT_DATE) > 0 
         AND (SELECT CURRENT_TIMESTAMP - MAX(last_updated) FROM target_orders WHERE load_date = CURRENT_DATE) < INTERVAL '4 hours'
        THEN 'HEALTHY'
        ELSE 'ISSUES DETECTED'
    END as overall_status;

