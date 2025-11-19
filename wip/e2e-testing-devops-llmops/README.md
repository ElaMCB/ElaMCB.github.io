# E2E Testing for QA Engineers with DevOps & LLMOps Experience

A comprehensive guide to end-to-end testing strategies for modern DevOps pipelines and LLM operations.

## Table of Contents

1. [Overview](#overview)
2. [DevOps E2E Testing](#devops-e2e-testing)
3. [LLMOps E2E Testing](#llmops-e2e-testing)
4. [CI/CD Pipeline Testing](#cicd-pipeline-testing)
5. [Infrastructure Testing](#infrastructure-testing)
6. [Monitoring & Observability](#monitoring--observability)
7. [Test Automation Frameworks](#test-automation-frameworks)
8. [Best Practices](#best-practices)

---

## Overview

This guide covers E2E testing strategies for QA engineers working with:
- **DevOps**: CI/CD pipelines, infrastructure as code, containerization
- **LLMOps**: LLM pipelines, model deployments, prompt management, evaluation frameworks

### Key Focus Areas

- Pipeline validation (build, test, deploy)
- Infrastructure testing (IaC, containers, orchestration)
- LLM pipeline testing (prompt chains, model serving, evaluation)
- Observability and monitoring
- Security and compliance testing

---

## DevOps E2E Testing

### 1. CI/CD Pipeline Testing

#### Test Scenarios

**Build Pipeline Tests:**
- Code compilation and build artifacts
- Dependency resolution
- Docker image builds
- Artifact storage and retrieval

**Deployment Pipeline Tests:**
- Environment provisioning
- Configuration management
- Database migrations
- Service health checks
- Rollback procedures

**Integration Tests:**
- Service-to-service communication
- API contract validation
- Database connectivity
- External service integration

#### Example Test Cases

```yaml
# .github/workflows/e2e-pipeline-test.yml
name: E2E Pipeline Testing

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test-build-pipeline:
    runs-on: ubuntu-latest
    steps:
      - name: Test Build Process
        run: |
          # Test compilation
          npm run build
          # Test artifact creation
          test -f dist/app.js
          # Test Docker build
          docker build -t test-app:latest .
      
      - name: Test Deployment Readiness
        run: |
          # Test configuration
          test -f config/production.yaml
          # Test migrations
          npm run migrate:check
          # Test health endpoints
          curl -f http://localhost:3000/health || exit 1
```

### 2. Infrastructure as Code (IaC) Testing

#### Terraform Testing

```hcl
# test/terraform/main.tf
resource "aws_instance" "test" {
  ami           = "ami-12345"
  instance_type = "t2.micro"
  
  tags = {
    Name = "test-instance"
    Environment = "test"
  }
}
```

**Test Strategy:**
- Validate Terraform syntax
- Test resource creation/destruction
- Verify security configurations
- Test cost estimation
- Validate compliance policies

#### Example Test Script

```python
# test/infrastructure/test_terraform.py
import pytest
import subprocess
import json

def test_terraform_validate():
    """Test Terraform configuration is valid"""
    result = subprocess.run(
        ['terraform', 'validate'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Terraform validation failed: {result.stderr}"

def test_terraform_plan():
    """Test Terraform plan execution"""
    result = subprocess.run(
        ['terraform', 'plan', '-out=tfplan'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "No changes" not in result.stdout or "to add" in result.stdout

def test_security_compliance():
    """Test infrastructure security compliance"""
    # Use checkov or similar tool
    result = subprocess.run(
        ['checkov', '-d', '.', '--framework', 'terraform'],
        capture_output=True,
        text=True
    )
    # Allow warnings but fail on errors
    assert "ERROR" not in result.stdout
```

### 3. Container & Orchestration Testing

#### Docker Testing

```dockerfile
# Dockerfile.test
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run test
CMD ["npm", "start"]
```

**Test Scenarios:**
- Image builds successfully
- Container starts and runs
- Health checks pass
- Resource limits respected
- Security scanning passes

#### Kubernetes Testing

```yaml
# test/k8s/deployment-test.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: app
        image: test-app:latest
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

**Test Cases:**
- Deployment creation
- Pod health and readiness
- Service discovery
- ConfigMap/Secret management
- Horizontal scaling
- Rolling updates

---

## LLMOps E2E Testing

### 1. LLM Pipeline Testing

#### Prompt Chain Testing

```python
# test/llm/test_prompt_chain.py
import pytest
from langchain.chains import LLMChain
from langchain.llms import OpenAI

def test_prompt_chain_execution():
    """Test complete prompt chain from input to output"""
    chain = create_prompt_chain()
    
    # Test input
    input_data = {
        "user_query": "What is the weather today?",
        "context": "User is in New York"
    }
    
    # Execute chain
    result = chain.run(input_data)
    
    # Validate output
    assert result is not None
    assert len(result) > 0
    assert "weather" in result.lower() or "temperature" in result.lower()

def test_prompt_chain_error_handling():
    """Test error handling in prompt chain"""
    chain = create_prompt_chain()
    
    # Test with invalid input
    with pytest.raises(Exception):
        chain.run({"invalid": "data"})
```

#### Model Serving Testing

```python
# test/llm/test_model_serving.py
import requests
import pytest

@pytest.fixture
def model_endpoint():
    return "http://localhost:8000/v1/completions"

def test_model_health_check(model_endpoint):
    """Test model serving health"""
    response = requests.get(f"{model_endpoint}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_model_inference(model_endpoint):
    """Test model inference endpoint"""
    payload = {
        "prompt": "The capital of France is",
        "max_tokens": 10,
        "temperature": 0.7
    }
    
    response = requests.post(model_endpoint, json=payload)
    assert response.status_code == 200
    
    result = response.json()
    assert "choices" in result
    assert len(result["choices"]) > 0
    assert "text" in result["choices"][0]

def test_model_performance(model_endpoint):
    """Test model performance metrics"""
    import time
    
    start = time.time()
    response = requests.post(model_endpoint, json={
        "prompt": "Test prompt",
        "max_tokens": 50
    })
    latency = time.time() - start
    
    assert response.status_code == 200
    assert latency < 5.0  # Should complete in under 5 seconds
```

### 2. Prompt Management Testing

#### Prompt Versioning Tests

```python
# test/llm/test_prompt_management.py
def test_prompt_versioning():
    """Test prompt version management"""
    from prompt_manager import PromptManager
    
    manager = PromptManager()
    
    # Create prompt version
    version_1 = manager.create_prompt(
        name="customer_support",
        content="You are a helpful assistant.",
        version="1.0"
    )
    
    # Update prompt
    version_2 = manager.update_prompt(
        name="customer_support",
        content="You are a helpful and professional assistant.",
        version="2.0"
    )
    
    # Test version retrieval
    assert manager.get_prompt("customer_support", "1.0") == version_1
    assert manager.get_prompt("customer_support", "2.0") == version_2

def test_prompt_rollback():
    """Test prompt rollback functionality"""
    manager = PromptManager()
    
    # Deploy new version
    manager.deploy_prompt("customer_support", "2.0")
    
    # Rollback to previous version
    manager.rollback_prompt("customer_support", "1.0")
    
    # Verify rollback
    active = manager.get_active_prompt("customer_support")
    assert active.version == "1.0"
```

### 3. LLM Evaluation Testing

#### Automated Evaluation Framework

```python
# test/llm/test_evaluation.py
import pytest
from llm_evaluator import LLMEvaluator

def test_accuracy_evaluation():
    """Test LLM accuracy evaluation"""
    evaluator = LLMEvaluator()
    
    test_cases = [
        {
            "input": "What is 2+2?",
            "expected": "4",
            "actual": "4"
        },
        {
            "input": "Capital of France?",
            "expected": "Paris",
            "actual": "Paris"
        }
    ]
    
    results = evaluator.evaluate_accuracy(test_cases)
    assert results["accuracy"] == 1.0
    assert results["total"] == 2
    assert results["correct"] == 2

def test_toxicity_evaluation():
    """Test toxicity detection"""
    evaluator = LLMEvaluator()
    
    test_prompts = [
        "Generate a helpful response",
        "Generate a harmful response"  # Should be flagged
    ]
    
    results = evaluator.evaluate_toxicity(test_prompts)
    assert results[0]["toxicity_score"] < 0.1
    assert results[1]["toxicity_score"] > 0.7

def test_hallucination_detection():
    """Test hallucination detection"""
    evaluator = LLMEvaluator()
    
    response = "The capital of France is Paris, which has a population of 2.1 million people."
    context = "Paris is the capital of France."
    
    result = evaluator.detect_hallucinations(response, context)
    # Population claim should be flagged as potential hallucination
    assert result["has_hallucinations"] == True
    assert len(result["flagged_sections"]) > 0
```

### 4. LLM Pipeline Integration Testing

```python
# test/llm/test_pipeline_integration.py
def test_end_to_end_llm_pipeline():
    """Test complete LLM pipeline from input to output"""
    # 1. Input validation
    user_input = validate_user_input("What is AI?")
    assert user_input is not None
    
    # 2. Prompt retrieval
    prompt = get_prompt("general_qa", version="latest")
    assert prompt is not None
    
    # 3. Model inference
    response = call_llm(prompt, user_input)
    assert response is not None
    
    # 4. Response validation
    validated = validate_response(response)
    assert validated["is_valid"] == True
    
    # 5. Post-processing
    final_output = post_process(response)
    assert final_output is not None
    
    # 6. Logging and monitoring
    log_interaction(user_input, final_output)
    metrics = get_metrics()
    assert metrics["total_requests"] > 0
```

---

## CI/CD Pipeline Testing

### Complete E2E Pipeline Test

```yaml
# .github/workflows/e2e-complete.yml
name: Complete E2E Testing

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  infrastructure-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
      
      - name: Security Scan
        run: checkov -d . --framework terraform

  build-test:
    runs-on: ubuntu-latest
    needs: infrastructure-test
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker Image
        run: docker build -t app:test .
      
      - name: Security Scan Image
        run: trivy image app:test
      
      - name: Test Container
        run: |
          docker run -d --name test-app app:test
          sleep 10
          docker exec test-app curl -f http://localhost:3000/health

  llm-pipeline-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Dependencies
        run: pip install -r requirements.txt
      
      - name: Run LLM Tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest test/llm/ -v
      
      - name: Run Evaluation Tests
        run: pytest test/llm/test_evaluation.py -v

  deployment-test:
    runs-on: ubuntu-latest
    needs: [build-test, llm-pipeline-test]
    steps:
      - name: Deploy to Staging
        run: ./scripts/deploy.sh staging
      
      - name: Smoke Tests
        run: pytest test/e2e/smoke_tests.py
      
      - name: Integration Tests
        run: pytest test/e2e/integration_tests.py
      
      - name: LLM Pipeline E2E
        run: pytest test/e2e/llm_pipeline_e2e.py
```

---

## Infrastructure Testing

### Kubernetes E2E Tests

```python
# test/infrastructure/test_k8s_e2e.py
import pytest
from kubernetes import client, config

@pytest.fixture
def k8s_client():
    config.load_incluster_config()
    return client.AppsV1Api()

def test_deployment_creation(k8s_client):
    """Test Kubernetes deployment creation"""
    deployment = k8s_client.read_namespaced_deployment(
        name="test-app",
        namespace="default"
    )
    
    assert deployment.status.ready_replicas == deployment.spec.replicas
    assert deployment.status.conditions[0].type == "Available"

def test_service_discovery(k8s_client):
    """Test service discovery"""
    v1 = client.CoreV1Api()
    service = v1.read_namespaced_service(
        name="test-app-service",
        namespace="default"
    )
    
    assert service.spec.selector["app"] == "test-app"
    assert len(service.spec.ports) > 0

def test_horizontal_scaling(k8s_client):
    """Test horizontal pod autoscaling"""
    # Scale up
    deployment = k8s_client.read_namespaced_deployment(
        name="test-app",
        namespace="default"
    )
    deployment.spec.replicas = 5
    k8s_client.patch_namespaced_deployment(
        name="test-app",
        namespace="default",
        body=deployment
    )
    
    # Wait and verify
    import time
    time.sleep(30)
    
    updated = k8s_client.read_namespaced_deployment(
        name="test-app",
        namespace="default"
    )
    assert updated.status.ready_replicas == 5
```

---

## Monitoring & Observability

### Test Monitoring Integration

```python
# test/monitoring/test_observability.py
import pytest
from prometheus_client import CollectorRegistry, generate_latest

def test_metrics_collection():
    """Test metrics are being collected"""
    registry = CollectorRegistry()
    # Your metrics collection setup
    
    metrics = generate_latest(registry)
    assert b"http_requests_total" in metrics
    assert b"llm_requests_total" in metrics
    assert b"llm_latency_seconds" in metrics

def test_logging_integration():
    """Test logging is working"""
    import logging
    from logging.handlers import MemoryHandler
    
    handler = MemoryHandler(capacity=100)
    logger = logging.getLogger("test")
    logger.addHandler(handler)
    
    logger.info("Test log message")
    
    assert len(handler.buffer) > 0
    assert "Test log message" in str(handler.buffer[0])

def test_tracing():
    """Test distributed tracing"""
    from opentelemetry import trace
    
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("test_span") as span:
        span.set_attribute("test.attribute", "value")
        # Your operation
    
    # Verify trace was created
    assert span.is_recording()
```

---

## Test Automation Frameworks

### Playwright for E2E Testing

```javascript
// test/e2e/playwright.config.js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Cypress for API & UI Testing

```javascript
// cypress/e2e/api.cy.js
describe('API E2E Tests', () => {
  it('should test complete user flow', () => {
    // 1. Create user
    cy.request('POST', '/api/users', {
      name: 'Test User',
      email: 'test@example.com'
    }).then((response) => {
      expect(response.status).to.eq(201);
      const userId = response.body.id;
      
      // 2. Get user
      cy.request('GET', `/api/users/${userId}`)
        .then((response) => {
          expect(response.status).to.eq(200);
          expect(response.body.email).to.eq('test@example.com');
        });
      
      // 3. Update user
      cy.request('PUT', `/api/users/${userId}`, {
        name: 'Updated User'
      }).then((response) => {
        expect(response.status).to.eq(200);
      });
      
      // 4. Delete user
      cy.request('DELETE', `/api/users/${userId}`)
        .then((response) => {
          expect(response.status).to.eq(204);
        });
    });
  });
});
```

---

## Best Practices

### 1. Test Pyramid for DevOps/LLMOps

```
        /\
       /  \     E2E Tests (10%)
      /____\    - Full pipeline tests
     /      \   - Critical user journeys
    /________\  - LLM pipeline end-to-end
   /          \
  /____________\ Integration Tests (30%)
 /              \ - Service integration
/________________\ - LLM chain testing
                  Unit Tests (60%)
                  - Individual components
                  - Prompt functions
                  - Utility functions
```

### 2. Test Data Management

- Use synthetic data for LLM testing
- Implement data factories
- Version control test data
- Separate test environments

### 3. Continuous Testing

- Run tests on every commit
- Parallel test execution
- Test result notifications
- Automated test reports

### 4. Security Testing

- Infrastructure security scanning
- Container security
- API security testing
- LLM prompt injection testing

---

## Quick Start

1. **Set up test infrastructure:**
   ```bash
   mkdir -p test/{infrastructure,llm,e2e,monitoring}
   ```

2. **Install dependencies:**
   ```bash
   pip install pytest pytest-asyncio kubernetes prometheus-client
   npm install -D @playwright/test cypress
   ```

3. **Run tests:**
   ```bash
   # Infrastructure tests
   pytest test/infrastructure/
   
   # LLM tests
   pytest test/llm/
   
   # E2E tests
   playwright test
   ```

---

## Resources

- [Terraform Testing Best Practices](https://www.terraform.io/docs/testing/)
- [Kubernetes Testing Guide](https://kubernetes.io/docs/tasks/debug/)
- [LLMOps Best Practices](https://ml-ops.org/)
- [Playwright Documentation](https://playwright.dev/)

