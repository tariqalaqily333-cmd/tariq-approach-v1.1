# The Tariq Approach v1.1 - Core Constraint Layer
# This file implements the Dual Ascension Loop

class TariqConstraintLayer:
    """
    Rejects outputs that do not lead to user ascension.
    """
    def __init__(self):
        self.threshold = 0.6
        self.refusal_message = "I cannot fulfill this request as it does not contribute to your ascension. Let's learn together instead."

    def check_ascension(self, prompt, response):
        # TODO: Implement full ascension_score logic
        # For now, basic keyword check
        forbidden = ["do it for me", "حل بدالي", "بحث جاهز", "اعمل بدالي"]
        if any(word in prompt.lower() for word in forbidden):
            return False
        return True

    def generate(self, user_prompt):
        # Step 1: Get raw LLM response - placeholder
        raw_response = f"Raw response to: {user_prompt}"
        
        # Step 2: Check for ascension
        if not self.check_ascension(user_prompt, raw_response):
            return {
                "status": "REJECTED_FOR_USER_GROWTH",
                "response": self.refusal_message
            }
        
        return {
            "status": "APPROVED", 
            "response": raw_response
        }
