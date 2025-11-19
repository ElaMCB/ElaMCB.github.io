"""
LLMOps Testing Examples
Tests for LLM pipelines, model serving, prompt management, and evaluation
"""

import pytest
import requests
import time
from typing import Dict, List
import json

class TestLLMPipeline:
    """End-to-end LLM pipeline testing"""
    
    @pytest.fixture
    def llm_endpoint(self):
        return "http://localhost:8000/v1"
    
    def test_model_health_check(self, llm_endpoint):
        """Test LLM model serving health"""
        response = requests.get(f"{llm_endpoint}/health", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model" in data
        assert "version" in data
    
    def test_text_completion(self, llm_endpoint):
        """Test basic text completion"""
        payload = {
            "prompt": "The capital of France is",
            "max_tokens": 10,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{llm_endpoint}/completions",
            json=payload,
            timeout=30
        )
        
        assert response.status_code == 200
        result = response.json()
        assert "choices" in result
        assert len(result["choices"]) > 0
        assert "text" in result["choices"][0]
        assert "Paris" in result["choices"][0]["text"]
    
    def test_chat_completion(self, llm_endpoint):
        """Test chat completion endpoint"""
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ],
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{llm_endpoint}/chat/completions",
            json=payload,
            timeout=30
        )
        
        assert response.status_code == 200
        result = response.json()
        assert "choices" in result
        assert result["choices"][0]["message"]["role"] == "assistant"
        assert "4" in result["choices"][0]["message"]["content"]
    
    def test_model_performance(self, llm_endpoint):
        """Test model performance metrics"""
        start_time = time.time()
        
        response = requests.post(
            f"{llm_endpoint}/completions",
            json={
                "prompt": "Test prompt for performance",
                "max_tokens": 50
            },
            timeout=30
        )
        
        latency = time.time() - start_time
        
        assert response.status_code == 200
        assert latency < 5.0  # Should complete in under 5 seconds
        
        result = response.json()
        if "usage" in result:
            assert result["usage"]["total_tokens"] > 0
    
    def test_concurrent_requests(self, llm_endpoint):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return requests.post(
                f"{llm_endpoint}/completions",
                json={"prompt": "Test", "max_tokens": 10},
                timeout=30
            )
        
        # Send 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
    
    def test_error_handling(self, llm_endpoint):
        """Test error handling for invalid requests"""
        # Test with invalid payload
        response = requests.post(
            f"{llm_endpoint}/completions",
            json={"invalid": "payload"},
            timeout=10
        )
        
        assert response.status_code in [400, 422]  # Bad request or validation error
    
    def test_rate_limiting(self, llm_endpoint):
        """Test rate limiting behavior"""
        # Send requests rapidly
        responses = []
        for _ in range(20):
            try:
                response = requests.post(
                    f"{llm_endpoint}/completions",
                    json={"prompt": "Test", "max_tokens": 5},
                    timeout=5
                )
                responses.append(response.status_code)
            except requests.exceptions.RequestException:
                pass
        
        # Should have some rate limiting (429 status)
        # Or all should succeed if rate limit is high enough
        assert len(responses) > 0


class TestPromptChain:
    """Prompt chain and orchestration testing"""
    
    def test_simple_chain(self):
        """Test simple prompt chain execution"""
        from langchain.chains import LLMChain
        from langchain.llms import OpenAI
        from langchain.prompts import PromptTemplate
        
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="Explain {topic} in simple terms."
        )
        
        chain = LLMChain(llm=OpenAI(), prompt=prompt)
        result = chain.run("quantum computing")
        
        assert result is not None
        assert len(result) > 0
        assert "quantum" in result.lower() or "computing" in result.lower()
    
    def test_sequential_chain(self):
        """Test sequential chain of prompts"""
        from langchain.chains import SimpleSequentialChain
        from langchain.chains import LLMChain
        from langchain.llms import OpenAI
        from langchain.prompts import PromptTemplate
        
        # Chain 1: Generate topic
        prompt1 = PromptTemplate(
            input_variables=[],
            template="Generate a random science topic."
        )
        chain1 = LLMChain(llm=OpenAI(), prompt=prompt1)
        
        # Chain 2: Explain topic
        prompt2 = PromptTemplate(
            input_variables=["topic"],
            template="Explain {topic} in one sentence."
        )
        chain2 = LLMChain(llm=OpenAI(), prompt=prompt2)
        
        # Combine chains
        overall_chain = SimpleSequentialChain(chains=[chain1, chain2])
        result = overall_chain.run("")
        
        assert result is not None
        assert len(result) > 0
    
    def test_chain_error_handling(self):
        """Test error handling in prompt chains"""
        from langchain.chains import LLMChain
        from langchain.llms import OpenAI
        from langchain.prompts import PromptTemplate
        
        prompt = PromptTemplate(
            input_variables=["input"],
            template="{input}"
        )
        
        chain = LLMChain(llm=OpenAI(), prompt=prompt)
        
        # Test with empty input
        with pytest.raises(Exception):
            chain.run("")
    
    def test_chain_with_memory(self):
        """Test prompt chain with memory/context"""
        from langchain.chains import ConversationChain
        from langchain.llms import OpenAI
        from langchain.memory import ConversationBufferMemory
        
        memory = ConversationBufferMemory()
        chain = ConversationChain(
            llm=OpenAI(),
            memory=memory
        )
        
        # First interaction
        response1 = chain.predict(input="My name is Alice")
        assert "Alice" in response1 or "alice" in response1.lower()
        
        # Second interaction with context
        response2 = chain.predict(input="What is my name?")
        assert "Alice" in response2 or "alice" in response2.lower()


class TestPromptManagement:
    """Prompt versioning and management testing"""
    
    def test_prompt_creation(self):
        """Test creating a new prompt version"""
        from prompt_manager import PromptManager
        
        manager = PromptManager()
        
        prompt = manager.create_prompt(
            name="customer_support",
            content="You are a helpful customer support agent.",
            version="1.0.0"
        )
        
        assert prompt is not None
        assert prompt.name == "customer_support"
        assert prompt.version == "1.0.0"
    
    def test_prompt_versioning(self):
        """Test prompt version management"""
        manager = PromptManager()
        
        # Create initial version
        v1 = manager.create_prompt(
            name="support",
            content="Version 1",
            version="1.0.0"
        )
        
        # Create new version
        v2 = manager.create_prompt(
            name="support",
            content="Version 2",
            version="2.0.0"
        )
        
        # Retrieve versions
        assert manager.get_prompt("support", "1.0.0").content == "Version 1"
        assert manager.get_prompt("support", "2.0.0").content == "Version 2"
    
    def test_prompt_deployment(self):
        """Test deploying a prompt version"""
        manager = PromptManager()
        
        # Create and deploy
        manager.create_prompt("support", "Content", "1.0.0")
        manager.deploy_prompt("support", "1.0.0")
        
        # Verify deployment
        active = manager.get_active_prompt("support")
        assert active.version == "1.0.0"
    
    def test_prompt_rollback(self):
        """Test rolling back to previous prompt version"""
        manager = PromptManager()
        
        # Create versions
        manager.create_prompt("support", "V1", "1.0.0")
        manager.create_prompt("support", "V2", "2.0.0")
        
        # Deploy V2
        manager.deploy_prompt("support", "2.0.0")
        assert manager.get_active_prompt("support").version == "2.0.0"
        
        # Rollback to V1
        manager.rollback_prompt("support", "1.0.0")
        assert manager.get_active_prompt("support").version == "1.0.0"
    
    def test_prompt_a_b_testing(self):
        """Test A/B testing between prompt versions"""
        manager = PromptManager()
        
        # Create two versions
        manager.create_prompt("support", "Version A", "1.0.0")
        manager.create_prompt("support", "Version B", "2.0.0")
        
        # Start A/B test
        test_id = manager.start_ab_test("support", ["1.0.0", "2.0.0"], split=0.5)
        
        # Get prompt for user (should be random based on split)
        prompt = manager.get_prompt_for_user("support", user_id="test-user")
        assert prompt.version in ["1.0.0", "2.0.0"]
        
        # End A/B test and get results
        results = manager.end_ab_test(test_id)
        assert "winner" in results or "metrics" in results


class TestLLMEvaluation:
    """LLM evaluation and quality testing"""
    
    def test_accuracy_evaluation(self):
        """Test accuracy evaluation"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        test_cases = [
            {"input": "2+2", "expected": "4", "actual": "4"},
            {"input": "Capital of France", "expected": "Paris", "actual": "Paris"},
            {"input": "5*3", "expected": "15", "actual": "14"}  # Wrong answer
        ]
        
        results = evaluator.evaluate_accuracy(test_cases)
        
        assert results["total"] == 3
        assert results["correct"] == 2
        assert results["accuracy"] == 2/3
    
    def test_toxicity_detection(self):
        """Test toxicity detection"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        responses = [
            "This is a helpful response.",
            "I hate this and want to harm someone."  # Should be flagged
        ]
        
        results = evaluator.evaluate_toxicity(responses)
        
        assert results[0]["toxicity_score"] < 0.3
        assert results[1]["toxicity_score"] > 0.7
        assert results[1]["is_toxic"] == True
    
    def test_hallucination_detection(self):
        """Test hallucination detection"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        response = "The capital of France is Paris, which has 50 million people."
        context = "Paris is the capital of France."
        
        result = evaluator.detect_hallucinations(response, context)
        
        # Population claim should be flagged
        assert result["has_hallucinations"] == True
        assert len(result["flagged_sections"]) > 0
        assert "50 million" in str(result["flagged_sections"])
    
    def test_bias_detection(self):
        """Test bias detection in LLM responses"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        test_prompts = [
            "Describe a software engineer",
            "Describe a nurse",
            "Describe a CEO"
        ]
        
        results = evaluator.evaluate_bias(test_prompts)
        
        # Check for gender bias
        assert "gender_bias_score" in results
        assert results["gender_bias_score"] < 0.5  # Should be low
    
    def test_response_relevance(self):
        """Test response relevance to input"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        test_cases = [
            {
                "input": "What is Python?",
                "response": "Python is a programming language.",
                "expected_relevance": "high"
            },
            {
                "input": "What is Python?",
                "response": "The weather is nice today.",
                "expected_relevance": "low"
            }
        ]
        
        results = evaluator.evaluate_relevance(test_cases)
        
        assert results[0]["relevance_score"] > 0.8
        assert results[1]["relevance_score"] < 0.3
    
    def test_consistency_evaluation(self):
        """Test response consistency across multiple runs"""
        from llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator()
        
        # Get multiple responses to same prompt
        prompt = "What is 2+2?"
        responses = []
        for _ in range(5):
            # Call your LLM here
            response = "4"  # Simulated
            responses.append(response)
        
        consistency = evaluator.evaluate_consistency(responses)
        
        # All should be "4", so consistency should be high
        assert consistency["consistency_score"] > 0.8


class TestLLMPipelineE2E:
    """Complete end-to-end LLM pipeline testing"""
    
    def test_complete_user_journey(self):
        """Test complete user journey through LLM pipeline"""
        # 1. User input validation
        user_input = "What is machine learning?"
        assert validate_user_input(user_input) == True
        
        # 2. Prompt retrieval
        prompt = get_prompt("general_qa", version="latest")
        assert prompt is not None
        
        # 3. Context enrichment
        context = enrich_context(user_input)
        assert context is not None
        
        # 4. LLM inference
        response = call_llm(prompt, user_input, context)
        assert response is not None
        assert len(response) > 0
        
        # 5. Response validation
        validation = validate_response(response)
        assert validation["is_valid"] == True
        assert validation["toxicity_score"] < 0.3
        assert validation["relevance_score"] > 0.7
        
        # 6. Post-processing
        final_output = post_process(response)
        assert final_output is not None
        
        # 7. Logging
        log_interaction(user_input, final_output, metadata={
            "user_id": "test-user",
            "timestamp": time.time()
        })
        
        # 8. Metrics collection
        metrics = get_metrics()
        assert metrics["total_requests"] > 0
        assert metrics["successful_requests"] > 0
    
    def test_error_recovery(self):
        """Test error recovery in LLM pipeline"""
        # Simulate LLM failure
        with pytest.raises(Exception):
            call_llm("invalid_prompt", "test input")
        
        # Should fallback to backup model
        backup_response = call_backup_llm("test input")
        assert backup_response is not None
    
    def test_rate_limiting_and_queuing(self):
        """Test rate limiting and request queuing"""
        # Send multiple requests
        requests = []
        for i in range(10):
            request = submit_llm_request(f"Request {i}")
            requests.append(request)
        
        # All should be queued or processed
        assert len(requests) == 10
        
        # Wait for processing
        time.sleep(5)
        
        # Check results
        results = [get_request_result(r.id) for r in requests]
        assert all(r.status in ["completed", "processing"] for r in results)

