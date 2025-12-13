# Project 1: Data Lakehouse Migration

## Overview

Migration of enterprise data warehouse from **Redshift/DBT** to modern **AWS Lakehouse architecture** using **S3, Glue, Databricks, and Unity Catalog**.

## Business Context

- **Challenge**: Legacy Redshift warehouse was expensive ($80K/month) and couldn't scale for growing data volumes
- **Solution**: Migrated to cost-effective lakehouse architecture with open table formats
- **Result**: 60% cost reduction, 3x query performance improvement, improved data governance

## Architecture

### Before: Redshift + DBT Architecture
```
Source Systems → DBT Transformations → Redshift Warehouse → BI Tools
```

### After: Lakehouse Architecture
```
Source Systems → S3 (Bronze) → Glue ETL → Delta Lake (Silver/Gold) → Databricks SQL → BI Tools
                                    ↓
                            Unity Catalog (Governance)
```

## Key Components

### 1. Data Ingestion (Bronze Layer)
- Raw data landing in S3 with partitioning by date/source
- Schema-on-read approach for flexibility
- Data retention policies

### 2. Data Processing (Silver Layer)
- ETL jobs using AWS Glue and Databricks
- Data cleaning, deduplication, and standardization
- Delta Lake tables for ACID transactions

### 3. Data Modeling (Gold Layer)
- Curated datasets for analytics
- Star schema for dimensional modeling
- Optimized for query performance

### 4. Data Governance (Unity Catalog)
- Centralized metadata management
- Column-level security and access control
- Data lineage tracking

## Implementation

### Migration Strategy

1. **Assessment Phase**
   - Analyzed existing DBT models and dependencies
   - Identified data volumes and access patterns
   - Cost analysis and ROI calculation

2. **Design Phase**
   - Designed lakehouse architecture
   - Created data model mapping (Redshift → Delta Lake)
   - Defined governance policies

3. **Migration Phase**
   - Incremental migration with zero downtime
   - Parallel run period for validation
   - Cutover to new system

4. **Optimization Phase**
   - Query performance tuning
   - Cost optimization
   - User training and documentation

## Code Examples

### DBT Model (Before)
```sql
-- models/fact_sales.sql
{{ config(materialized='table') }}

SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    amount,
    quantity
FROM {{ ref('stg_orders') }}
```

### Delta Lake Table (After)
```python
# Databricks notebook: create_fact_sales.py
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder \
    .appName("CreateFactSales") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read from Silver layer
silver_df = spark.read.format("delta").load("s3://data-lake/silver/orders")

# Transform and create Gold layer
fact_sales = silver_df.select(
    "order_id",
    "customer_id", 
    "product_id",
    "order_date",
    "amount",
    "quantity"
).withColumn("load_timestamp", current_timestamp())

# Write to Delta Lake with partitioning
fact_sales.write \
    .format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .partitionBy("order_date") \
    .save("s3://data-lake/gold/fact_sales")

# Register in Unity Catalog
spark.sql("""
    CREATE TABLE IF NOT EXISTS main.gold.fact_sales
    USING DELTA
    LOCATION 's3://data-lake/gold/fact_sales'
""")
```

### Unity Catalog Setup
```python
# Unity Catalog configuration
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Create catalog
w.catalogs.create(
    name="main",
    comment="Main data catalog for enterprise data"
)

# Create schema
w.schemas.create(
    catalog_name="main",
    name="gold",
    comment="Gold layer for curated analytics data"
)

# Grant access
w.grants.update(
    securable_type="TABLE",
    full_name="main.gold.fact_sales",
    changes=[
        {
            "principal": "data_analysts",
            "add": ["SELECT"]
        }
    ]
)
```

### Incremental Load with Delta Lake
```python
# Incremental ETL with merge operation
from delta.tables import DeltaTable

# Read existing Delta table
target_table = DeltaTable.forPath(spark, "s3://data-lake/gold/fact_sales")

# Read new data from source
new_data = spark.read.format("delta").load("s3://data-lake/silver/orders") \
    .filter("load_date = current_date()")

# Merge operation (upsert)
target_table.alias("target") \
    .merge(
        new_data.alias("source"),
        "target.order_id = source.order_id"
    ) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()
```

## Performance Optimizations

### 1. Partitioning Strategy
- Partitioned by `order_date` for time-based queries
- Z-ordering on `customer_id` for customer analytics
- Bloom filters on frequently filtered columns

### 2. Data Skipping
- Leveraged Delta Lake's data skipping capabilities
- Reduced scan time by 80% for filtered queries

### 3. Caching
- Cached frequently accessed tables in Databricks
- Reduced query latency from seconds to milliseconds

## Cost Optimization

### Before (Redshift)
- **Monthly Cost**: $80,000
- **Storage**: $25/TB/month
- **Compute**: Always-on clusters

### After (Lakehouse)
- **Monthly Cost**: $32,000 (60% reduction)
- **Storage**: S3 $23/TB/month (standard)
- **Compute**: On-demand Databricks clusters
- **Savings**: $48,000/month

## Data Quality & Validation

### Validation Checks
```python
# data_quality_checks.py
from great_expectations import DataContext

context = DataContext()

# Define expectations
expectation_suite = context.create_expectation_suite(
    expectation_suite_name="fact_sales_quality"
)

# Add expectations
expectation_suite.expect_column_values_to_not_be_null("order_id")
expectation_suite.expect_column_values_to_be_between("amount", 0, 1000000)
expectation_suite.expect_table_row_count_to_be_between(1000, 10000000)

# Validate data
validation_result = context.run_validation_operator(
    "action_list_operator",
    assets_to_validate=[("fact_sales", expectation_suite)]
)
```

## Migration Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Monthly Cost** | $80,000 | $32,000 | 60% reduction |
| **Query Performance** | 30s avg | 10s avg | 3x faster |
| **Data Freshness** | Daily | Hourly | 24x improvement |
| **Storage Scalability** | Limited | Unlimited | ∞ |
| **Data Governance** | Manual | Automated | 100% coverage |

## Lessons Learned

1. **Incremental Migration**: Migrated table by table to minimize risk
2. **Parallel Run**: Ran both systems in parallel for 3 months for validation
3. **User Training**: Comprehensive training on Databricks SQL and Delta Lake
4. **Documentation**: Created detailed data dictionary and lineage documentation
5. **Monitoring**: Set up comprehensive monitoring and alerting

## Files

- `migration_plan.md` - Detailed migration plan and timeline
- `dbt_to_delta_mapping.md` - Mapping of DBT models to Delta tables
- `unity_catalog_setup.py` - Unity Catalog configuration
- `data_quality_checks.py` - Data validation framework
- `cost_analysis.xlsx` - Cost comparison and ROI analysis

## Technologies Used

- **AWS**: S3, Glue, IAM, CloudTrail
- **Databricks**: Delta Lake, Unity Catalog, SQL Analytics
- **Python**: PySpark, Delta Lake API
- **SQL**: Databricks SQL, Spark SQL
- **Tools**: Great Expectations, dbt (legacy)

---

**Status**: ✅ Completed  
**Duration**: 6 months  
**Team Size**: 4 data engineers


