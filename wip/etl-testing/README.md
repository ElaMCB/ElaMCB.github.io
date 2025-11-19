# ETL Testing Resources

This directory contains comprehensive ETL testing resources for data-heavy QA engineers.

## Contents

### 1. ETL Test Plan Template (`ETL_TEST_PLAN_TEMPLATE.md`)
A complete test plan template covering:
- Test strategy and approach
- Test cases for Extract, Transform, and Load phases
- Data quality testing
- Performance testing
- Defect management
- Test metrics and reporting

### 2. SQL Test Cases (`example-test-cases.sql`)
Ready-to-use SQL queries for:
- Source data validation
- Transformation verification
- Load validation
- Data quality checks
- Performance monitoring

### 3. Python Test Cases (`example-test-cases.py`)
Python/pytest test functions for:
- Automated ETL testing
- Data validation
- Business rule testing
- Integration testing

## Quick Start

### Using SQL Test Cases

1. Connect to your database
2. Copy relevant SQL queries from `example-test-cases.sql`
3. Modify table/column names to match your schema
4. Execute and review results

Example:
```sql
-- Run record count reconciliation
-- Copy query #10 from example-test-cases.sql
-- Modify table names
-- Execute
```

### Using Python Test Cases

1. Install dependencies:
```bash
pip install pytest pandas psycopg2-binary
```

2. Update connection fixtures in `example-test-cases.py`

3. Run tests:
```bash
pytest etl-testing/example-test-cases.py -v
```

## Test Categories

### Extract Phase
- Source data availability
- Schema validation
- Data quality checks
- Duplicate detection

### Transform Phase
- Business rule validation
- Data type conversions
- Aggregation validation
- Join and lookup verification

### Load Phase
- Record count reconciliation
- Data integrity validation
- Incremental load logic
- Data freshness checks

### Data Quality
- Completeness checks
- Accuracy validation
- Consistency verification
- Uniqueness checks

### Performance
- Load time validation
- Throughput measurement
- Resource utilization

## Customization

### For Your ETL Pipeline

1. **Update Table Names**
   - Replace `source_orders` with your source table
   - Replace `target_orders` with your target table

2. **Modify Business Rules**
   - Update calculation logic in test cases
   - Adjust validation thresholds

3. **Add Custom Validations**
   - Add project-specific test cases
   - Include domain-specific rules

## Best Practices

1. **Run Tests Regularly**
   - Daily: Critical path tests
   - Weekly: Full test suite
   - Before deployment: Complete regression

2. **Monitor Test Results**
   - Track pass/fail rates
   - Set up alerts for failures
   - Review trends over time

3. **Maintain Test Data**
   - Keep test data fresh
   - Include edge cases
   - Cover all business scenarios

4. **Document Findings**
   - Log all test results
   - Track defects
   - Update test cases as needed

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: ETL Tests

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install pytest pandas psycopg2-binary
      - name: Run ETL tests
        env:
          DB_HOST: ${{ secrets.DB_HOST }}
          DB_USER: ${{ secrets.DB_USER }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: pytest etl-testing/example-test-cases.py -v
```

## Additional Resources

- [Great Expectations](https://greatexpectations.io/) - Data quality framework
- [dbt](https://www.getdbt.com/) - Data transformation testing
- [Soda](https://www.soda.io/) - Data quality monitoring

## Support

For questions or improvements, please refer to the main project documentation or create an issue.

