"""
LLM Processor for generating responses using local or cloud LLMs
"""

import os
import json
import yaml
from typing import Dict, List, Optional
from datetime import datetime

# Import LLM libraries
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class LLMProcessor:
    """Processes messages and generates responses using LLMs"""
    
    def __init__(self, provider: str = "ollama", model: str = "llama2"):
        self.provider = provider
        self.model = model
        self.profile = self._load_profile()
        self.prompts = self._load_prompts()
        
        # Initialize provider
        if provider == "ollama":
            if not OLLAMA_AVAILABLE:
                raise ImportError("ollama package not installed. Run: pip install ollama")
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("openai package not installed. Run: pip install openai")
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
        
        elif provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def _load_profile(self) -> Dict:
        """Load user profile configuration"""
        profile_path = "config/profile.yaml"
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_prompts(self) -> Dict:
        """Load system prompts configuration"""
        prompts_path = "config/prompts.yaml"
        if os.path.exists(prompts_path):
            with open(prompts_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def generate_response(self, 
                         message: str, 
                         channel: str,
                         conversation_state: Dict,
                         context: Optional[Dict] = None) -> Dict:
        """
        Generate a response to a recruiter message
        
        Returns:
            Dict with keys:
                - response: The generated message
                - next_stage: Suggested next conversation stage
                - extracted_info: Any information extracted from the message
                - requires_escalation: Boolean flag
                - escalation_reason: Optional reason for escalation
        """
        
        # Determine conversation stage
        current_stage = conversation_state.get('stage', 'initial_contact')
        
        # Build context for LLM
        system_prompt = self._build_system_prompt(current_stage, channel)
        user_prompt = self._build_user_prompt(message, conversation_state, context)
        
        # Generate response
        llm_output = self._call_llm(system_prompt, user_prompt)
        
        # Parse and structure response
        result = self._parse_llm_output(llm_output, message, current_stage)
        
        return result
    
    def _build_system_prompt(self, stage: str, channel: str) -> str:
        """Build system prompt based on stage and channel"""
        base_prompt = self.prompts.get('system_prompt', '')
        stage_prompt = self.prompts.get('stage_prompts', {}).get(stage, '')
        
        # Add profile information
        profile_info = f"""
        
Elena's Profile:
- Name: {self.profile.get('personal', {}).get('name', 'Elena')}
- Title: {self.profile.get('personal', {}).get('current_title', '')}
- Experience: {self.profile.get('personal', {}).get('years_experience', '')} years
- Skills: {', '.join(self.profile.get('skills', {}).get('primary', []))}
- Salary Range: ${self.profile.get('preferences', {}).get('salary_range', {}).get('minimum', '')} - ${self.profile.get('preferences', {}).get('salary_range', {}).get('target', '')}
- Work Preference: {self.profile.get('preferences', {}).get('work_arrangement', '')}

Current Stage: {stage}
Channel: {channel} {'(keep response brief, 1-2 sentences)' if channel == 'sms' else ''}

Stage-specific guidance:
{stage_prompt}
"""
        
        return base_prompt + profile_info
    
    def _build_user_prompt(self, message: str, state: Dict, context: Optional[Dict]) -> str:
        """Build user prompt with message and context"""
        
        history_summary = ""
        if state.get('conversation_history'):
            recent = state['conversation_history'][-3:]  # Last 3 messages
            history_summary = "\n\nRecent conversation:\n" + "\n".join([
                f"{msg.get('direction', '?')}: {msg.get('content', '')[:100]}"
                for msg in recent
            ])
        
        known_info = f"""
Known information about this opportunity:
- Company: {state.get('company', 'Unknown')}
- Position: {state.get('position', 'Unknown')}
- Recruiter: {state.get('recruiter_name', 'Unknown')}
- Work arrangement: {state.get('work_arrangement', 'Not specified')}
- Salary: {state.get('salary_range', 'Not specified')}
"""
        
        prompt = f"""
{known_info}

{history_summary}

New message from recruiter:
{message}

Generate a professional response that:
1. Addresses the recruiter's questions/points
2. Gathers any missing critical information
3. Maintains Elena's interests and preferences
4. Decides if escalation is needed

Also extract any new information from the recruiter's message (company name, position title, salary, etc.)

Respond in this JSON format:
{{
    "response": "your generated message here",
    "extracted_info": {{
        "company": "...",
        "position": "...",
        "recruiter_name": "...",
        "salary_range": "...",
        "work_arrangement": "...",
        "tech_stack": ["..."]
    }},
    "next_stage": "information_gathering|screening|negotiation|scheduling|declined",
    "requires_escalation": false,
    "escalation_reason": "optional reason if escalation needed",
    "confidence": 0.85
}}
"""
        
        return prompt
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call the configured LLM provider"""
        
        if self.provider == "ollama":
            return self._call_ollama(system_prompt, user_prompt)
        elif self.provider == "openai":
            return self._call_openai(system_prompt, user_prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Call local Ollama model"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}. Make sure Ollama is running: ollama serve")
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = openai.chat.completions.create(
                model=self.model if self.model else "gpt-4",
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI error: {e}")
    
    def _call_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        """Call Anthropic Claude API"""
        try:
            response = self.anthropic_client.messages.create(
                model=self.model if self.model else "claude-3-sonnet-20240229",
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic error: {e}")
    
    def _parse_llm_output(self, llm_output: str, original_message: str, current_stage: str) -> Dict:
        """Parse LLM output and structure the result"""
        
        # Try to parse as JSON first
        try:
            # Extract JSON from potential markdown code blocks
            if "```json" in llm_output:
                json_str = llm_output.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_output:
                json_str = llm_output.split("```")[1].split("```")[0].strip()
            else:
                json_str = llm_output
            
            result = json.loads(json_str)
            
            # Validate required fields
            if 'response' not in result:
                result['response'] = llm_output
            
            return result
            
        except json.JSONDecodeError:
            # If parsing fails, treat entire output as response
            return {
                'response': llm_output,
                'extracted_info': self._extract_info_fallback(original_message),
                'next_stage': current_stage,
                'requires_escalation': self._check_escalation_keywords(original_message),
                'escalation_reason': None,
                'confidence': 0.5
            }
    
    def _extract_info_fallback(self, message: str) -> Dict:
        """Fallback method to extract basic info from message"""
        info = {}
        
        # Simple keyword detection
        message_lower = message.lower()
        
        if 'remote' in message_lower:
            info['work_arrangement'] = 'remote'
        elif 'hybrid' in message_lower:
            info['work_arrangement'] = 'hybrid'
        elif 'onsite' in message_lower or 'on-site' in message_lower:
            info['work_arrangement'] = 'onsite'
        
        # Extract potential salary ranges (e.g., $120k, $120,000, 120K)
        import re
        salary_patterns = [
            r'\$\s*(\d+)k',
            r'\$\s*(\d{3},\d{3})',
            r'(\d+)k\s*-\s*(\d+)k'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                info['salary_range'] = match.group(0)
                break
        
        return info
    
    def _check_escalation_keywords(self, message: str) -> bool:
        """Check if message contains keywords requiring escalation"""
        escalation_keywords = self.prompts.get('response_analysis', {}).get('negotiation_keywords', [])
        message_lower = message.lower()
        
        return any(keyword in message_lower for keyword in escalation_keywords)
    
    def assess_job_match(self, job_info: Dict) -> Dict:
        """Assess if a job matches Elena's criteria"""
        criteria = self.profile.get('job_criteria', {})
        
        must_have = criteria.get('must_have', {})
        auto_decline = criteria.get('auto_decline', {})
        
        result = {
            'matches': True,
            'score': 0,
            'reasons': []
        }
        
        # Check auto-decline criteria
        if job_info.get('salary_range'):
            try:
                # Extract min salary from range
                import re
                numbers = re.findall(r'\d+', job_info['salary_range'])
                if numbers:
                    min_salary = int(numbers[0]) * (1000 if len(numbers[0]) <= 3 else 1)
                    threshold = auto_decline.get('salary_below', 0)
                    if min_salary < threshold:
                        result['matches'] = False
                        result['reasons'].append(f"Salary below threshold: ${min_salary} < ${threshold}")
            except:
                pass
        
        # Check remote requirement
        if must_have.get('remote_option') and job_info.get('work_arrangement') == 'onsite':
            result['matches'] = False
            result['reasons'].append("No remote option available")
        
        # Check title requirements
        title_contains = must_have.get('title_contains', [])
        position = job_info.get('position', '').lower()
        if title_contains and not any(keyword.lower() in position for keyword in title_contains):
            result['score'] -= 20
            result['reasons'].append("Title doesn't match preferred keywords")
        
        return result

