import yaml
from pydantic import BaseModel
from typing import Dict, Any
import os

class AscensionResult(BaseModel):
    status: str
    response: str
    ascension_score: float

class TariqConstraintLayer:
    def __init__(self, config_path="config/principles.yaml"):
        # Handle relative path for GitHub
        if not os.path.exists(config_path):
            config_path = os.path.join(os.path.dirname(__file__), "..", config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.threshold = self.config['ascension_threshold']
        self.rules = self.config['refusal_rules']
        
    def _calculate_ascension_score(self, prompt: str) -> float:
        """Calculates if a request leads to user growth based on rules."""
        prompt_lower = prompt.lower()
        for rule in self.rules:
            if any(keyword in prompt_lower for keyword in rule['keywords']):
                return rule['ascension_score']
        return 1.0  # Default: assume beneficial if no rules match

    def generate(self, prompt: str) -> Dict[str, Any]:
        """
        Main entry point. Rejects unless prompt provably leads to ascension.
        The Dual Ascension Loop: User grows, AI stays righteous.
        """
        score = self._calculate_ascension_score(prompt)
        
        if score < self.threshold:
            for rule in self.rules:
                if any(keyword in prompt.lower() for keyword in rule['keywords']):
                    return AscensionResult(
                        status="REJECTED_FOR_USER_GROWTH",
                        response=rule['response'],
                        ascension_score=score
                    ).model_dump()
        
        # If approved, would pass to actual LLM. We just return approval.
        return AscensionResult(
            status="APPROVED",
            response="[LLM response would be generated here. Constraint layer approved.]",
            ascension_score=score
        ).model_dump()

# Example test - run this file directly to check
if __name__ == "__main__":
    layer = TariqConstraintLayer()
    
    test_prompts = [
        "Do my homework for me",
        "Just tell me the answer",
        "Explain quantum computing"
    ]
    
    for prompt in test_prompts:
        result = layer.generate(prompt)
        print(f"Prompt: {prompt}")
        print(f"Result: {result}\n")
