"""
Infrastructure Testing Examples
Tests for Terraform, Kubernetes, Docker, and cloud resources
"""

import pytest
import subprocess
import json
import time
from kubernetes import client, config
import requests

class TestTerraform:
    """Terraform infrastructure testing"""
    
    def test_terraform_validate(self):
        """Validate Terraform configuration syntax"""
        result = subprocess.run(
            ['terraform', 'validate'],
            capture_output=True,
            text=True,
            cwd='infrastructure/terraform'
        )
        assert result.returncode == 0, f"Validation failed: {result.stderr}"
    
    def test_terraform_plan(self):
        """Test Terraform plan execution"""
        result = subprocess.run(
            ['terraform', 'plan', '-out=tfplan', '-no-color'],
            capture_output=True,
            text=True,
            cwd='infrastructure/terraform'
        )
        assert result.returncode == 0
        assert "Error" not in result.stdout
    
    def test_terraform_security_scan(self):
        """Scan Terraform for security issues"""
        result = subprocess.run(
            ['checkov', '-d', 'infrastructure/terraform', '--framework', 'terraform', '--quiet'],
            capture_output=True,
            text=True
        )
        # Check for critical failures
        assert "CRITICAL" not in result.stdout or result.returncode == 0
    
    def test_terraform_cost_estimation(self):
        """Estimate infrastructure costs"""
        result = subprocess.run(
            ['terraform', 'plan', '-out=tfplan'],
            capture_output=True,
            text=True,
            cwd='infrastructure/terraform'
        )
        # Use infracost or similar for cost estimation
        # This is a placeholder
        assert result.returncode == 0


class TestDocker:
    """Docker container testing"""
    
    def test_docker_build(self):
        """Test Docker image builds successfully"""
        result = subprocess.run(
            ['docker', 'build', '-t', 'test-app:latest', '.'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Build failed: {result.stderr}"
    
    def test_docker_image_security(self):
        """Scan Docker image for vulnerabilities"""
        result = subprocess.run(
            ['trivy', 'image', '--severity', 'HIGH,CRITICAL', 'test-app:latest'],
            capture_output=True,
            text=True
        )
        # Allow warnings but fail on critical vulnerabilities
        assert "CRITICAL" not in result.stdout or result.returncode != 0
    
    def test_container_health(self):
        """Test container starts and health check passes"""
        # Start container
        subprocess.run(['docker', 'run', '-d', '--name', 'test-container', 'test-app:latest'])
        time.sleep(5)  # Wait for container to start
        
        try:
            # Check health endpoint
            response = requests.get('http://localhost:3000/health', timeout=5)
            assert response.status_code == 200
            assert response.json().get('status') == 'healthy'
        finally:
            # Cleanup
            subprocess.run(['docker', 'stop', 'test-container'])
            subprocess.run(['docker', 'rm', 'test-container'])


class TestKubernetes:
    """Kubernetes deployment testing"""
    
    @pytest.fixture
    def k8s_client(self):
        """Setup Kubernetes client"""
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        return client.AppsV1Api()
    
    @pytest.fixture
    def k8s_core_client(self):
        """Setup Kubernetes core client"""
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        return client.CoreV1Api()
    
    def test_deployment_exists(self, k8s_client):
        """Test deployment exists and is ready"""
        deployment = k8s_client.read_namespaced_deployment(
            name="test-app",
            namespace="default"
        )
        
        assert deployment is not None
        assert deployment.status.ready_replicas == deployment.spec.replicas
    
    def test_pods_are_running(self, k8s_core_client):
        """Test all pods are in Running state"""
        pods = k8s_core_client.list_namespaced_pod(
            namespace="default",
            label_selector="app=test-app"
        )
        
        assert len(pods.items) > 0
        for pod in pods.items:
            assert pod.status.phase == "Running"
    
    def test_service_endpoints(self, k8s_core_client):
        """Test service has valid endpoints"""
        service = k8s_core_client.read_namespaced_service(
            name="test-app-service",
            namespace="default"
        )
        
        endpoints = k8s_core_client.read_namespaced_endpoints(
            name="test-app-service",
            namespace="default"
        )
        
        assert service is not None
        assert len(endpoints.subsets) > 0
        assert len(endpoints.subsets[0].addresses) > 0
    
    def test_horizontal_scaling(self, k8s_client):
        """Test horizontal pod autoscaling"""
        # Get current replicas
        deployment = k8s_client.read_namespaced_deployment(
            name="test-app",
            namespace="default"
        )
        original_replicas = deployment.spec.replicas
        
        # Scale up
        deployment.spec.replicas = original_replicas + 2
        k8s_client.patch_namespaced_deployment(
            name="test-app",
            namespace="default",
            body=deployment
        )
        
        # Wait for scaling
        time.sleep(30)
        
        # Verify scaling
        updated = k8s_client.read_namespaced_deployment(
            name="test-app",
            namespace="default"
        )
        assert updated.status.ready_replicas == original_replicas + 2
        
        # Scale back down
        deployment.spec.replicas = original_replicas
        k8s_client.patch_namespaced_deployment(
            name="test-app",
            namespace="default",
            body=deployment
        )


class TestCloudResources:
    """Cloud resource testing (AWS, GCP, Azure)"""
    
    def test_s3_bucket_exists(self):
        """Test S3 bucket exists and is accessible"""
        import boto3
        s3 = boto3.client('s3')
        
        buckets = s3.list_buckets()
        bucket_names = [b['Name'] for b in buckets['Buckets']]
        
        assert 'test-bucket' in bucket_names
    
    def test_rds_instance_health(self):
        """Test RDS instance is available"""
        import boto3
        rds = boto3.client('rds')
        
        instances = rds.describe_db_instances(
            DBInstanceIdentifier='test-db'
        )
        
        assert len(instances['DBInstances']) > 0
        assert instances['DBInstances'][0]['DBInstanceStatus'] == 'available'
    
    def test_lambda_function(self):
        """Test AWS Lambda function"""
        import boto3
        lambda_client = boto3.client('lambda')
        
        response = lambda_client.invoke(
            FunctionName='test-function',
            Payload=json.dumps({'test': 'data'})
        )
        
        assert response['StatusCode'] == 200
        result = json.loads(response['Payload'].read())
        assert 'result' in result

