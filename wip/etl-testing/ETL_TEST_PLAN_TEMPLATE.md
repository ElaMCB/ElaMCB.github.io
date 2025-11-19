# ETL Test Plan Template

## 1. Test Plan Overview

**Project Name:** [ETL Pipeline Name]  
**Test Plan Version:** 1.0  
**Date:** [Date]  
**Prepared By:** [Your Name]  
**Last Updated:** [Date]

### 1.1 Purpose
This document outlines the test strategy, test cases, and validation approach for the [ETL Pipeline Name] data pipeline.

### 1.2 Scope
- Source system: [Source System Name]
- Target system: [Target System Name]
- Data pipeline: [Pipeline Name]
- Testing period: [Start Date] to [End Date]

### 1.3 Test Objectives
- Validate data extraction from source systems
- Verify data transformation logic accuracy
- Ensure data integrity during load process
- Confirm data quality standards are met
- Validate performance and scalability

---

## 2. Test Environment

### 2.1 Environments
- **Development:** [Environment Details]
- **Staging:** [Environment Details]
- **Production:** [Environment Details]

### 2.2 Test Data
- **Source:** [Source Data Location]
- **Test Data Sets:** [Test Data Description]
- **Data Refresh Frequency:** [Daily/Weekly/etc.]

### 2.3 Tools and Technologies
- ETL Platform: [Airflow/Databricks/etc.]
- Database: [PostgreSQL/MySQL/BigQuery/etc.]
- Testing Framework: [Pytest/Great Expectations/etc.]
- Monitoring: [Grafana/DataDog/etc.]

---

## 3. Test Strategy

### 3.1 Testing Levels

#### 3.1.1 Unit Testing
- Individual transformation functions
- Business rule validations
- Data type conversions

#### 3.1.2 Integration Testing
- End-to-end pipeline execution
- Source to target data flow
- Error handling and recovery

#### 3.1.3 System Testing
- Full pipeline with production-like data
- Performance and load testing
- Data quality validation

#### 3.1.4 Regression Testing
- Existing functionality after changes
- Data consistency checks
- Performance benchmarks

### 3.2 Test Types

| Test Type | Description | Priority |
|-----------|-------------|----------|
| **Data Completeness** | Verify no data loss | High |
| **Data Accuracy** | Validate transformations | High |
| **Data Consistency** | Check referential integrity | High |
| **Data Timeliness** | Verify SLA compliance | Medium |
| **Data Validity** | Business rule validation | High |
| **Performance** | Load time and throughput | Medium |
| **Error Handling** | Failure scenarios | Medium |

---

## 4. Test Cases

### 4.1 Extract Phase Testing

#### TC-EXT-001: Source Data Availability
**Objective:** Verify source data is available and accessible

**Preconditions:**
- Source system is operational
- Network connectivity is established

**Test Steps:**
1. Connect to source system
2. Query source table/view
3. Verify record count > 0
4. Check data freshness (last update timestamp)

**Expected Results:**
- Connection successful
- Data is available
- Last update within expected timeframe

**SQL Validation:**
```sql
SELECT 
    COUNT(*) as record_count,
    MAX(last_updated) as last_update_time,
    CURRENT_TIMESTAMP - MAX(last_updated) as data_age
FROM source_table
WHERE load_date = CURRENT_DATE;
```

---

#### TC-EXT-002: Source Schema Validation
**Objective:** Verify source schema matches expected structure

**Test Steps:**
1. Query source table metadata
2. Compare with expected schema
3. Validate data types
4. Check for new/removed columns

**Expected Results:**
- All expected columns present
- Data types match specification
- No unexpected schema changes

---

#### TC-EXT-003: Source Data Quality Check
**Objective:** Identify data quality issues in source

**Test Steps:**
1. Check for null values in required fields
2. Validate data formats
3. Check for duplicates
4. Verify data ranges

**Expected Results:**
- No nulls in required fields
- Data formats valid
- No unexpected duplicates
- Values within expected ranges

**SQL Validation:**
```sql
-- Check nulls in required fields
SELECT 
    COUNT(*) as total_records,
    COUNT(required_field_1) as non_null_field_1,
    COUNT(required_field_2) as non_null_field_2,
    COUNT(*) - COUNT(required_field_1) as null_count_field_1
FROM source_table
WHERE load_date = CURRENT_DATE;

-- Check for duplicates
SELECT 
    key_field,
    COUNT(*) as duplicate_count
FROM source_table
WHERE load_date = CURRENT_DATE
GROUP BY key_field
HAVING COUNT(*) > 1;
```

---

### 4.2 Transform Phase Testing

#### TC-TRF-001: Business Rule Validation
**Objective:** Verify business logic transformations are correct

**Test Steps:**
1. Identify key business rules
2. Create test data with known inputs
3. Execute transformation
4. Validate output matches expected results

**Expected Results:**
- Calculations are accurate
- Business rules applied correctly
- Edge cases handled properly

**Example Test Case:**
```python
# Test revenue calculation
def test_revenue_calculation():
    # Given
    quantity = 10
    unit_price = 25.50
    discount = 0.10
    
    # When
    revenue = calculate_revenue(quantity, unit_price, discount)
    
    # Then
    expected = (10 * 25.50) * (1 - 0.10)  # 229.50
    assert revenue == expected
```

---

#### TC-TRF-002: Data Type Conversion
**Objective:** Verify data type conversions are correct

**Test Steps:**
1. Test string to numeric conversions
2. Test date format conversions
3. Test null handling
4. Test precision/scale for decimals

**Expected Results:**
- Conversions successful
- No data loss during conversion
- Nulls handled appropriately

---

#### TC-TRF-003: Data Aggregation Validation
**Objective:** Verify aggregation logic (SUM, AVG, COUNT, etc.)

**Test Steps:**
1. Calculate aggregations manually
2. Compare with ETL output
3. Test with different data volumes
4. Validate grouping logic

**SQL Validation:**
```sql
-- Compare manual calculation with ETL output
WITH manual_calc AS (
    SELECT 
        customer_id,
        SUM(order_amount) as manual_total,
        COUNT(*) as manual_count,
        AVG(order_amount) as manual_avg
    FROM source_orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
),
etl_output AS (
    SELECT 
        customer_id,
        total_amount,
        order_count,
        avg_order_amount
    FROM target_customer_summary
    WHERE snapshot_date = CURRENT_DATE
)
SELECT 
    m.customer_id,
    m.manual_total,
    e.total_amount,
    ABS(m.manual_total - e.total_amount) as difference
FROM manual_calc m
JOIN etl_output e ON m.customer_id = e.customer_id
WHERE ABS(m.manual_total - e.total_amount) > 0.01;  -- Tolerance for rounding
```

---

#### TC-TRF-004: Join and Lookup Validation
**Objective:** Verify joins and lookups return correct data

**Test Steps:**
1. Validate referential integrity
2. Check for orphaned records
3. Verify lookup table accuracy
4. Test left/right/inner join logic

**SQL Validation:**
```sql
-- Check for orphaned records (records without matching lookup)
SELECT 
    t.foreign_key,
    COUNT(*) as orphaned_count
FROM target_table t
LEFT JOIN lookup_table l ON t.foreign_key = l.lookup_key
WHERE l.lookup_key IS NULL
GROUP BY t.foreign_key;
```

---

### 4.3 Load Phase Testing

#### TC-LOD-001: Record Count Validation
**Objective:** Verify no data loss during load

**Test Steps:**
1. Count records in source
2. Count records in target
3. Compare counts
4. Account for filtered records

**Expected Results:**
- Source count matches target count (or within expected variance)
- Filtered records documented

**SQL Validation:**
```sql
-- Record count reconciliation
WITH source_count AS (
    SELECT COUNT(*) as src_count
    FROM source_table
    WHERE load_date = CURRENT_DATE
),
target_count AS (
    SELECT COUNT(*) as tgt_count
    FROM target_table
    WHERE load_date = CURRENT_DATE
),
filtered_count AS (
    SELECT COUNT(*) as filtered
    FROM source_table
    WHERE load_date = CURRENT_DATE
    AND status = 'INACTIVE'  -- Example filter condition
)
SELECT 
    s.src_count as source_records,
    t.tgt_count as target_records,
    f.filtered as filtered_records,
    s.src_count - f.filtered as expected_target,
    CASE 
        WHEN (s.src_count - f.filtered) = t.tgt_count THEN 'PASS'
        ELSE 'FAIL'
    END as validation_status
FROM source_count s
CROSS JOIN target_count t
CROSS JOIN filtered_count f;
```

---

#### TC-LOD-002: Data Integrity Validation
**Objective:** Verify data integrity constraints

**Test Steps:**
1. Check primary key uniqueness
2. Validate foreign key relationships
3. Check NOT NULL constraints
4. Verify check constraints

**SQL Validation:**
```sql
-- Check for duplicate primary keys
SELECT 
    primary_key,
    COUNT(*) as duplicate_count
FROM target_table
GROUP BY primary_key
HAVING COUNT(*) > 1;

-- Check foreign key integrity
SELECT 
    t.foreign_key,
    COUNT(*) as orphaned_count
FROM target_table t
LEFT JOIN referenced_table r ON t.foreign_key = r.primary_key
WHERE r.primary_key IS NULL
GROUP BY t.foreign_key;
```

---

#### TC-LOD-003: Incremental Load Validation
**Objective:** Verify incremental load logic

**Test Steps:**
1. Identify records that should be updated
2. Identify records that should be inserted
3. Verify update logic
4. Verify insert logic

**Expected Results:**
- Updates applied correctly
- New records inserted
- No duplicate records

**SQL Validation:**
```sql
-- Verify incremental load
WITH source_data AS (
    SELECT 
        key_field,
        updated_field,
        last_modified
    FROM source_table
    WHERE last_modified >= CURRENT_DATE - INTERVAL '1 day'
),
target_data AS (
    SELECT 
        key_field,
        updated_field,
        last_modified
    FROM target_table
    WHERE load_date = CURRENT_DATE
)
SELECT 
    'New Records' as check_type,
    COUNT(*) as count
FROM source_data s
LEFT JOIN target_data t ON s.key_field = t.key_field
WHERE t.key_field IS NULL

UNION ALL

SELECT 
    'Updated Records' as check_type,
    COUNT(*) as count
FROM source_data s
JOIN target_data t ON s.key_field = t.key_field
WHERE s.updated_field != t.updated_field;
```

---

#### TC-LOD-004: Data Freshness Validation
**Objective:** Verify data is up-to-date

**Test Steps:**
1. Check last update timestamp
2. Verify SLA compliance
3. Check data age

**Expected Results:**
- Data updated within SLA timeframe
- Last update timestamp is recent

**SQL Validation:**
```sql
SELECT 
    MAX(last_updated) as last_update_time,
    CURRENT_TIMESTAMP - MAX(last_updated) as data_age_hours,
    CASE 
        WHEN CURRENT_TIMESTAMP - MAX(last_updated) <= INTERVAL '1 hour' THEN 'PASS'
        ELSE 'FAIL'
    END as sla_status
FROM target_table
WHERE load_date = CURRENT_DATE;
```

---

### 4.4 Data Quality Testing

#### TC-DQ-001: Completeness Check
**Objective:** Verify required fields are populated

**Test Steps:**
1. Check for null values in required fields
2. Verify field population rates
3. Check for empty strings

**SQL Validation:**
```sql
SELECT 
    COUNT(*) as total_records,
    COUNT(required_field_1) as populated_field_1,
    COUNT(required_field_2) as populated_field_2,
    ROUND(100.0 * COUNT(required_field_1) / COUNT(*), 2) as completeness_pct
FROM target_table
WHERE load_date = CURRENT_DATE;
```

---

#### TC-DQ-002: Accuracy Check
**Objective:** Verify data values are accurate

**Test Steps:**
1. Validate numeric ranges
2. Check date ranges
3. Verify format compliance
4. Validate business rules

**SQL Validation:**
```sql
-- Check for values outside expected range
SELECT 
    COUNT(*) as out_of_range_count
FROM target_table
WHERE load_date = CURRENT_DATE
AND (
    numeric_field < 0 
    OR numeric_field > 1000000
    OR date_field < '2020-01-01'
    OR date_field > CURRENT_DATE
);
```

---

#### TC-DQ-003: Consistency Check
**Objective:** Verify data consistency across systems

**Test Steps:**
1. Compare key metrics across systems
2. Verify referential integrity
3. Check for data drift

**SQL Validation:**
```sql
-- Compare metrics across systems
SELECT 
    'System A' as source,
    COUNT(*) as record_count,
    SUM(amount) as total_amount
FROM system_a_table
WHERE date = CURRENT_DATE

UNION ALL

SELECT 
    'System B' as source,
    COUNT(*) as record_count,
    SUM(amount) as total_amount
FROM system_b_table
WHERE date = CURRENT_DATE;
```

---

#### TC-DQ-004: Uniqueness Check
**Objective:** Verify no duplicate records

**Test Steps:**
1. Check for duplicate primary keys
2. Check for duplicate business keys
3. Verify deduplication logic

**SQL Validation:**
```sql
-- Find duplicates
SELECT 
    business_key,
    COUNT(*) as duplicate_count
FROM target_table
GROUP BY business_key
HAVING COUNT(*) > 1;
```

---

### 4.5 Performance Testing

#### TC-PERF-001: Load Time Validation
**Objective:** Verify ETL completes within SLA

**Test Steps:**
1. Monitor ETL job execution time
2. Compare with baseline
3. Check for performance degradation

**Expected Results:**
- ETL completes within SLA timeframe
- Performance within acceptable range

---

#### TC-PERF-002: Throughput Validation
**Objective:** Verify data processing rate

**Test Steps:**
1. Measure records processed per second
2. Compare with baseline
3. Identify bottlenecks

**Expected Results:**
- Throughput meets requirements
- No significant degradation

---

## 5. Test Execution

### 5.1 Test Schedule
- **Unit Tests:** Run on every code commit
- **Integration Tests:** Run daily in staging
- **System Tests:** Run weekly
- **Regression Tests:** Run before production deployment

### 5.2 Test Execution Log

| Test Case ID | Test Case Name | Status | Executed By | Date | Notes |
|--------------|----------------|--------|-------------|------|-------|
| TC-EXT-001 | Source Data Availability | PASS | [Name] | [Date] | - |
| TC-EXT-002 | Source Schema Validation | PASS | [Name] | [Date] | - |

---

## 6. Defect Management

### 6.1 Defect Severity Levels
- **Critical:** Pipeline failure, data loss
- **High:** Incorrect transformations, data quality issues
- **Medium:** Performance issues, minor data discrepancies
- **Low:** Documentation, cosmetic issues

### 6.2 Defect Log Template

| Defect ID | Test Case | Severity | Description | Status | Assigned To | Date |
|-----------|-----------|----------|-------------|--------|-------------|------|
| DEF-001 | TC-TRF-001 | High | Revenue calculation incorrect | Open | [Name] | [Date] |

---

## 7. Test Metrics

### 7.1 Test Coverage
- **Test Coverage:** [X]%
- **Requirements Coverage:** [X]%
- **Code Coverage:** [X]%

### 7.2 Quality Metrics
- **Defect Density:** [X] defects per 1000 lines of code
- **Defect Detection Rate:** [X]%
- **Test Pass Rate:** [X]%

---

## 8. Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | [Name] | | |
| Data Engineer | [Name] | | |
| Business Analyst | [Name] | | |

---

## 9. Appendix

### 9.1 Test Data
- Test data location: [Path]
- Test data refresh: [Frequency]

### 9.2 References
- ETL Design Document: [Link]
- Data Dictionary: [Link]
- Business Rules: [Link]

