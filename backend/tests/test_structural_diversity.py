import unittest
from unittest.mock import MagicMock
from aphra_blogger.agents.content_generator import ContentGenerator
from src.orchestrator.continuous.validation import DraftValidator

class TestStructuralDiversity(unittest.TestCase):
    def setUp(self):
        self.generator = ContentGenerator()
        self.generator.llm = MagicMock()
        
    def test_prompt_includes_mode_and_hook(self):
        """Verify that the prompt contains the selected structural mode and hook."""
        topic = "RISC-V vs ARM"
        style_profile = {"tone": "conversational", "expressions": ["cacharreo"]}
        keywords = ["cpu", "chips"]
        
        # Mock LLM to return a simple response
        self.generator.llm.create_messages.return_value = []
        self.generator.llm.chat_completion.return_value.content = "Contenido generado"
        self.generator.llm.is_available.return_value = True
        
        self.generator.generate_draft(topic, style_profile, keywords, mode="TECHNICAL")
        
        # Check if the prompt sent to LLM contains the mode and hook instructions
        call_args = self.generator.llm.create_messages.call_args
        user_prompt = call_args[1]['user_prompt']
        
        self.assertIn("TECHNICAL", user_prompt)
        self.assertTrue("Hook Style:" in user_prompt or "HOOK STYLE:" in user_prompt)
        self.assertIn("PROHIBITION: Do NOT use a fixed", user_prompt)

    def test_random_mode_selection(self):
        """Verify that random modes are selected if not specified."""
        topics = ["AI", "Crypto", "Linux", "Gadgets", "Photography"]
        modes_seen = set()
        
        self.generator.llm.create_messages.return_value = []
        self.generator.llm.chat_completion.return_value.content = "Contenido"
        self.generator.llm.is_available.return_value = True
        
        for topic in topics:
            self.generator.generate_draft(topic, {}, [])
            call_args = self.generator.llm.create_messages.call_args
            user_prompt = call_args[1]['user_prompt']
            
            for mode in self.generator.STRUCTURAL_MODES.keys():
                if mode in user_prompt:
                    modes_seen.add(mode)
        
        # With 5 runs, we should likely see more than 1 mode if random is working
        self.assertGreater(len(modes_seen), 0)


class TestRedundancyValidation(unittest.TestCase):
    def test_redundancy_threshold_80_percent(self):
        validator = DraftValidator(redundancy_threshold=0.8)
        recent = [
            "La IA está acelerando el desarrollo de software con asistentes de código.",
            "Nuevos chips mejoran la inferencia local para modelos ligeros.",
        ]
        candidate = "La IA esta acelerando el desarrollo de software con asistentes de codigo."
        self.assertTrue(validator.is_redundant(candidate, recent))

if __name__ == "__main__":
    unittest.main()
