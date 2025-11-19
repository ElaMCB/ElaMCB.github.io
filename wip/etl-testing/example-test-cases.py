"""
ETL Testing Python Examples
Collection of reusable Python test functions for ETL validation
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal


# ============================================
# EXTRACT PHASE TESTING
# ============================================

def test_source_data_availability(source_connection):
    """TC-EXT-001: Verify source data is available and accessible"""
    query = """
        SELECT 
            COUNT(*) as record_count,
            MAX(last_updated) as last_update_time
        FROM source_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, source_connection)
    
    assert result['record_count'].iloc[0] > 0, "No records found in source"
    assert result['last_update_time'].iloc[0] is not None, "Last update time is null"
    
    # Check data freshness (should be within 24 hours)
    last_update = result['last_update_time'].iloc[0]
    age_hours = (datetime.now() - last_update).total_seconds() / 3600
    assert age_hours < 24, f"Data is stale: {age_hours:.2f} hours old"


def test_source_schema_validation(source_connection, expected_schema):
    """TC-EXT-002: Verify source schema matches expected structure"""
    query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'source_orders'
        ORDER BY ordinal_position
    """
    actual_schema = pd.read_sql(query, source_connection)
    
    # Compare with expected schema
    for _, expected_col in expected_schema.iterrows():
        actual_col = actual_schema[actual_schema['column_name'] == expected_col['column_name']]
        assert not actual_col.empty, f"Missing column: {expected_col['column_name']}"
        assert actual_col['data_type'].iloc[0] == expected_col['data_type'], \
            f"Data type mismatch for {expected_col['column_name']}"


def test_source_data_quality_nulls(source_connection):
    """TC-EXT-003: Check for null values in required fields"""
    query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(order_id) as non_null_order_id,
            COUNT(customer_id) as non_null_customer_id,
            COUNT(order_date) as non_null_order_date,
            COUNT(amount) as non_null_amount
        FROM source_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, source_connection)
    
    total = result['total_records'].iloc[0]
    assert result['non_null_order_id'].iloc[0] == total, "Null values found in order_id"
    assert result['non_null_customer_id'].iloc[0] == total, "Null values found in customer_id"
    assert result['non_null_order_date'].iloc[0] == total, "Null values found in order_date"
    assert result['non_null_amount'].iloc[0] == total, "Null values found in amount"


def test_source_data_quality_duplicates(source_connection):
    """TC-EXT-003: Check for duplicate records"""
    query = """
        SELECT order_id, COUNT(*) as duplicate_count
        FROM source_orders
        WHERE load_date = CURRENT_DATE
        GROUP BY order_id
        HAVING COUNT(*) > 1
    """
    duplicates = pd.read_sql(query, source_connection)
    
    assert duplicates.empty, f"Found {len(duplicates)} duplicate order_ids"


def test_source_data_quality_ranges(source_connection):
    """TC-EXT-003: Validate data ranges"""
    query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(CASE WHEN amount < 0 THEN 1 END) as negative_amounts,
            COUNT(CASE WHEN amount > 1000000 THEN 1 END) as excessive_amounts,
            COUNT(CASE WHEN order_date < '2020-01-01' THEN 1 END) as old_dates,
            COUNT(CASE WHEN order_date > CURRENT_DATE THEN 1 END) as future_dates
        FROM source_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, source_connection)
    
    assert result['negative_amounts'].iloc[0] == 0, "Found negative amounts"
    assert result['excessive_amounts'].iloc[0] == 0, "Found excessive amounts"
    assert result['old_dates'].iloc[0] == 0, "Found dates before 2020"
    assert result['future_dates'].iloc[0] == 0, "Found future dates"


# ============================================
# TRANSFORM PHASE TESTING
# ============================================

def test_business_rule_revenue_calculation():
    """TC-TRF-001: Verify revenue calculation business rule"""
    # Test data
    test_cases = [
        {
            'quantity': 10,
            'unit_price': 25.50,
            'discount': 0.10,
            'expected': Decimal('229.50')
        },
        {
            'quantity': 5,
            'unit_price': 100.00,
            'discount': 0.0,
            'expected': Decimal('500.00')
        },
        {
            'quantity': 1,
            'unit_price': 50.00,
            'discount': 0.25,
            'expected': Decimal('37.50')
        }
    ]
    
    for case in test_cases:
        revenue = calculate_revenue(
            case['quantity'],
            case['unit_price'],
            case['discount']
        )
        assert abs(revenue - case['expected']) < Decimal('0.01'), \
            f"Revenue calculation failed: expected {case['expected']}, got {revenue}"


def calculate_revenue(quantity, unit_price, discount_rate):
    """Business rule: revenue = (quantity * unit_price) * (1 - discount_rate)"""
    return Decimal(str(quantity)) * Decimal(str(unit_price)) * (Decimal('1') - Decimal(str(discount_rate)))


def test_data_aggregation(source_connection, target_connection):
    """TC-TRF-003: Verify aggregation logic"""
    # Manual calculation from source
    source_query = """
        SELECT 
            customer_id,
            COUNT(*) as order_count,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM source_orders
        WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE)
        GROUP BY customer_id
    """
    source_agg = pd.read_sql(source_query, source_connection)
    
    # ETL output from target
    target_query = """
        SELECT 
            customer_id,
            order_count,
            total_amount,
            avg_order_amount
        FROM target_customer_summary
        WHERE snapshot_date = CURRENT_DATE
    """
    target_agg = pd.read_sql(target_query, target_connection)
    
    # Compare
    merged = source_agg.merge(
        target_agg,
        on='customer_id',
        suffixes=('_source', '_target')
    )
    
    # Check order count
    assert all(merged['order_count_source'] == merged['order_count']), \
        "Order count mismatch"
    
    # Check total amount (with tolerance for rounding)
    amount_diff = (merged['total_amount_source'] - merged['total_amount']).abs()
    assert all(amount_diff < 0.01), \
        f"Total amount mismatch: {merged[amount_diff >= 0.01]}"


def test_join_referential_integrity(target_connection):
    """TC-TRF-004: Verify referential integrity after joins"""
    query = """
        SELECT 
            o.customer_id,
            COUNT(*) as orphaned_count
        FROM target_orders o
        LEFT JOIN target_customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
          AND o.load_date = CURRENT_DATE
        GROUP BY o.customer_id
    """
    orphans = pd.read_sql(query, target_connection)
    
    assert orphans.empty, f"Found {len(orphans)} orphaned records"


# ============================================
# LOAD PHASE TESTING
# ============================================

def test_record_count_reconciliation(source_connection, target_connection):
    """TC-LOD-001: Verify no data loss during load"""
    # Source count (with filters applied in ETL)
    source_query = """
        SELECT COUNT(*) as count
        FROM source_orders
        WHERE load_date = CURRENT_DATE
          AND status = 'ACTIVE'
    """
    source_count = pd.read_sql(source_query, source_connection)['count'].iloc[0]
    
    # Target count
    target_query = """
        SELECT COUNT(*) as count
        FROM target_orders
        WHERE load_date = CURRENT_DATE
    """
    target_count = pd.read_sql(target_query, target_connection)['count'].iloc[0]
    
    assert source_count == target_count, \
        f"Record count mismatch: source={source_count}, target={target_count}"


def test_primary_key_uniqueness(target_connection):
    """TC-LOD-002: Verify primary key uniqueness"""
    query = """
        SELECT order_id, COUNT(*) as duplicate_count
        FROM target_orders
        WHERE load_date = CURRENT_DATE
        GROUP BY order_id
        HAVING COUNT(*) > 1
    """
    duplicates = pd.read_sql(query, target_connection)
    
    assert duplicates.empty, f"Found {len(duplicates)} duplicate primary keys"


def test_incremental_load_logic(source_connection, target_connection):
    """TC-LOD-003: Verify incremental load logic"""
    # Get records that should be updated/inserted
    source_query = """
        SELECT 
            order_id,
            amount,
            status,
            last_modified
        FROM source_orders
        WHERE last_modified >= CURRENT_DATE - INTERVAL '1 day'
    """
    source_changes = pd.read_sql(source_query, source_connection)
    
    target_query = """
        SELECT 
            order_id,
            amount,
            status,
            last_modified
        FROM target_orders
        WHERE load_date = CURRENT_DATE
    """
    target_current = pd.read_sql(target_query, target_connection)
    
    # Check new records
    new_records = source_changes[
        ~source_changes['order_id'].isin(target_current['order_id'])
    ]
    
    # Check updated records
    merged = source_changes.merge(
        target_current,
        on='order_id',
        suffixes=('_source', '_target')
    )
    updated_records = merged[
        (merged['amount_source'] != merged['amount_target']) |
        (merged['status_source'] != merged['status_target'])
    ]
    
    # Verify new records are in target
    if not new_records.empty:
        new_in_target = target_current[
            target_current['order_id'].isin(new_records['order_id'])
        ]
        assert len(new_in_target) == len(new_records), \
            "Not all new records were inserted"
    
    # Verify updated records reflect changes
    if not updated_records.empty:
        for _, row in updated_records.iterrows():
            target_row = target_current[target_current['order_id'] == row['order_id']].iloc[0]
            assert target_row['amount'] == row['amount_source'], \
                f"Amount not updated for order_id {row['order_id']}"


def test_data_freshness(target_connection):
    """TC-LOD-004: Verify data is up-to-date"""
    query = """
        SELECT 
            MAX(last_updated) as last_update_time
        FROM target_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, target_connection)
    last_update = result['last_update_time'].iloc[0]
    
    if last_update:
        age_hours = (datetime.now() - last_update).total_seconds() / 3600
        assert age_hours < 1, f"Data is stale: {age_hours:.2f} hours old"


# ============================================
# DATA QUALITY TESTING
# ============================================

def test_completeness(target_connection):
    """TC-DQ-001: Verify required fields are populated"""
    query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(order_id) as order_id_complete,
            COUNT(customer_id) as customer_id_complete,
            COUNT(order_date) as order_date_complete,
            COUNT(amount) as amount_complete
        FROM target_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, target_connection)
    
    total = result['total_records'].iloc[0]
    assert result['order_id_complete'].iloc[0] == total, "order_id has nulls"
    assert result['customer_id_complete'].iloc[0] == total, "customer_id has nulls"
    assert result['order_date_complete'].iloc[0] == total, "order_date has nulls"
    assert result['amount_complete'].iloc[0] == total, "amount has nulls"


def test_accuracy_value_ranges(target_connection):
    """TC-DQ-002: Verify data values are within expected ranges"""
    query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(CASE WHEN amount < 0 THEN 1 END) as negative_amounts,
            COUNT(CASE WHEN amount > 1000000 THEN 1 END) as excessive_amounts,
            COUNT(CASE WHEN quantity < 0 THEN 1 END) as negative_quantities,
            COUNT(CASE WHEN discount_rate < 0 OR discount_rate > 1 THEN 1 END) as invalid_discounts
        FROM target_orders
        WHERE load_date = CURRENT_DATE
    """
    result = pd.read_sql(query, target_connection)
    
    assert result['negative_amounts'].iloc[0] == 0, "Found negative amounts"
    assert result['excessive_amounts'].iloc[0] == 0, "Found excessive amounts"
    assert result['negative_quantities'].iloc[0] == 0, "Found negative quantities"
    assert result['invalid_discounts'].iloc[0] == 0, "Found invalid discount rates"


def test_consistency_cross_table(target_connection):
    """TC-DQ-003: Verify data consistency across tables"""
    # Get order totals
    order_query = """
        SELECT 
            customer_id,
            COUNT(*) as order_count,
            SUM(amount) as total_amount
        FROM target_orders
        WHERE load_date = CURRENT_DATE
        GROUP BY customer_id
    """
    order_totals = pd.read_sql(order_query, target_connection)
    
    # Get customer summary
    summary_query = """
        SELECT 
            customer_id,
            order_count,
            total_amount
        FROM target_customer_summary
        WHERE snapshot_date = CURRENT_DATE
    """
    customer_summary = pd.read_sql(summary_query, target_connection)
    
    # Compare
    merged = order_totals.merge(
        customer_summary,
        on='customer_id',
        suffixes=('_orders', '_summary')
    )
    
    # Check consistency
    count_mismatch = merged[merged['order_count_orders'] != merged['order_count']]
    assert count_mismatch.empty, f"Order count mismatch for {len(count_mismatch)} customers"
    
    amount_diff = (merged['total_amount_orders'] - merged['total_amount']).abs()
    assert all(amount_diff < 0.01), \
        f"Amount mismatch for {len(merged[amount_diff >= 0.01])} customers"


def test_uniqueness_business_key(target_connection):
    """TC-DQ-004: Verify no duplicate business keys"""
    query = """
        SELECT 
            customer_id,
            order_date,
            product_id,
            COUNT(*) as duplicate_count
        FROM target_orders
        WHERE load_date = CURRENT_DATE
        GROUP BY customer_id, order_date, product_id
        HAVING COUNT(*) > 1
    """
    duplicates = pd.read_sql(query, target_connection)
    
    assert duplicates.empty, f"Found {len(duplicates)} duplicate business keys"


# ============================================
# PERFORMANCE TESTING
# ============================================

def test_load_performance(target_connection, max_load_time_minutes=30):
    """TC-PERF-001: Verify ETL completes within SLA"""
    query = """
        SELECT 
            load_date,
            COUNT(*) as records_loaded,
            MAX(load_timestamp) - MIN(load_timestamp) as load_duration
        FROM target_orders
        WHERE load_date = CURRENT_DATE
        GROUP BY load_date
    """
    result = pd.read_sql(query, target_connection)
    
    if not result.empty:
        load_duration = result['load_duration'].iloc[0]
        duration_minutes = load_duration.total_seconds() / 60
        
        assert duration_minutes < max_load_time_minutes, \
            f"Load time {duration_minutes:.2f} minutes exceeds SLA of {max_load_time_minutes} minutes"


# ============================================
# FIXTURES (for pytest)
# ============================================

@pytest.fixture
def source_connection():
    """Fixture for source database connection"""
    # Replace with your actual connection logic
    import psycopg2
    return psycopg2.connect(
        host='source-db-host',
        database='source_db',
        user='user',
        password='password'
    )


@pytest.fixture
def target_connection():
    """Fixture for target database connection"""
    # Replace with your actual connection logic
    import psycopg2
    return psycopg2.connect(
        host='target-db-host',
        database='target_db',
        user='user',
        password='password'
    )


@pytest.fixture
def expected_schema():
    """Fixture for expected schema definition"""
    return pd.DataFrame({
        'column_name': ['order_id', 'customer_id', 'order_date', 'amount'],
        'data_type': ['integer', 'integer', 'date', 'numeric'],
        'is_nullable': ['NO', 'NO', 'NO', 'NO']
    })


# ============================================
# USAGE EXAMPLE
# ============================================

"""
Run tests with pytest:
    pytest etl-testing/example-test-cases.py -v

Run specific test:
    pytest etl-testing/example-test-cases.py::test_source_data_availability -v

Run with coverage:
    pytest etl-testing/example-test-cases.py --cov=. --cov-report=html
"""

