import os
import unittest

from services.llm_service import generate_text


class LLMServiceTests(unittest.TestCase):
    def test_generate_text_falls_back_without_api_key(self):
        os.environ.pop("GROQ_API_KEY", None)
        response, tokens = generate_text([
            {"role": "user", "content": "Translate this to French: hello"}
        ])

        self.assertIsInstance(response, str)
        self.assertTrue(response)
        self.assertEqual(tokens, 0)


if __name__ == "__main__":
    unittest.main()
