# Quick Start Guide: E2E Testing for DevOps & LLMOps

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker
- Kubernetes cluster (or Kind for local testing)
- Terraform (for infrastructure testing)
- Access to LLM APIs (OpenAI, Anthropic, etc.)

## Setup

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install

# Install Playwright browsers
npx playwright install --with-deps
```

### 2. Configure Environment

Create `.env` file:

```bash
# LLM API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Infrastructure
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
KUBECONFIG=~/.kube/config

# Test Environment
BASE_URL=http://localhost:3000
STAGING_URL=https://staging.example.com
```

### 3. Run Tests

#### Infrastructure Tests
```bash
# Terraform tests
pytest test/infrastructure/test_terraform.py -v

# Docker tests
pytest test/infrastructure/test_docker.py -v

# Kubernetes tests
pytest test/infrastructure/test_k8s_e2e.py -v
```

#### LLM Pipeline Tests
```bash
# LLM pipeline tests
pytest test/llm/test_pipeline.py -v

# LLM evaluation tests
pytest test/llm/test_evaluation.py -v

# Prompt management tests
pytest test/llm/test_prompt_management.py -v
```

#### E2E Tests
```bash
# Playwright E2E tests
npx playwright test

# API E2E tests
pytest test/e2e/integration_tests.py -v
```

## Test Structure

```
test/
├── infrastructure/
│   ├── test_terraform.py
│   ├── test_docker.py
│   └── test_k8s_e2e.py
├── llm/
│   ├── test_pipeline.py
│   ├── test_evaluation.py
│   └── test_prompt_management.py
├── e2e/
│   ├── smoke_tests.py
│   ├── integration_tests.py
│   └── llm_pipeline_e2e.py
├── monitoring/
│   ├── test_metrics.py
│   └── test_logging.py
└── security/
    ├── test_prompt_injection.py
    └── test_api_security.py
```

## Common Test Scenarios

### 1. Test Complete Deployment Pipeline

```bash
# Run full pipeline test
pytest test/e2e/deployment_pipeline.py -v
```

### 2. Test LLM Pipeline End-to-End

```bash
# Test complete LLM flow
pytest test/e2e/llm_pipeline_e2e.py::test_complete_user_journey -v
```

### 3. Test Infrastructure Changes

```bash
# Test Terraform changes
terraform plan
pytest test/infrastructure/test_terraform.py -v
```

## CI/CD Integration

The provided GitHub Actions workflow (`.github/workflows/e2e-complete.yml`) runs all tests automatically on:
- Push to main/develop branches
- Pull requests
- Manual trigger

## Next Steps

1. Review test examples in `test-examples/` directory
2. Customize tests for your specific infrastructure
3. Add your LLM pipeline tests
4. Set up monitoring and alerting
5. Integrate with your CI/CD pipeline

