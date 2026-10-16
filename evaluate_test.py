
import os
import asyncio
import time

from dotenv import load_dotenv
from google import genai
from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric

load_dotenv()


class GeminiModel(DeepEvalBaseLLM):
    def __init__(self, model_name="gemini-3.6-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY .env file mein nahi mili.")

        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    def load_model(self):
        return self.client

    def generate(self, prompt: str, schema=None) -> str:
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                if not response.text:
                    raise RuntimeError("Gemini ne empty response diya.")

                return response.text

            except Exception as error:
                message = str(error)
                temporary = any(
                    term in message
                    for term in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED")
                )

                if not temporary or attempt == 2:
                    raise

                wait_seconds = 2 ** (attempt + 1)
                print(
                    f"Gemini temporarily busy. "
                    f"Retry {attempt + 1}/2 in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)

        raise RuntimeError("Gemini retries complete.")

    async def a_generate(self, prompt: str, schema=None) -> str:
        return await asyncio.to_thread(self.generate, prompt, schema)

    def get_model_name(self) -> str:
        return self.model_name


def main():
    print("Starting Gemini + DeepEval evaluation...")

    model = GeminiModel()

    test_case = LLMTestCase(
        input="Explain artificial intelligence in simple words.",
        actual_output=(
            "Artificial Intelligence allows computers to perform tasks "
            "that usually require human intelligence, such as understanding "
            "language, recognizing images, and solving problems."
        ),
        expected_output=(
            "Artificial Intelligence allows computers to perform tasks "
            "that normally require human intelligence."
        ),
        retrieval_context=[
            "Artificial Intelligence allows computers to perform tasks "
            "that normally require human intelligence, including language "
            "understanding, image recognition, and problem solving."
        ],
    )

    metrics = [
        AnswerRelevancyMetric(
            threshold=0.7,
            model=model,
            include_reason=True,
        ),
        FaithfulnessMetric(
            threshold=0.7,
            model=model,
            include_reason=True,
        ),
    ]

    results = []

    for metric in metrics:
        name = metric.__class__.__name__
        print(f"\nEvaluating: {name}")

        try:
            metric.measure(test_case)
            passed = metric.is_successful()

            result = {
                "metric": name,
                "score": metric.score,
                "passed": passed,
                "reason": metric.reason,
                "error": None,
            }

            print(f"Score: {metric.score}")
            print(f"Passed: {passed}")
            print(f"Reason: {metric.reason}")

        except Exception as error:
            result = {
                "metric": name,
                "score": None,
                "passed": False,
                "reason": None,
                "error": f"{type(error).__name__}: {error}",
            }

            print(f"Evaluation unavailable: {result['error']}")

        results.append(result)

    with open("evaluation_metrics.json", "w", encoding="utf-8") as file:
        import json
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("\nResults saved to evaluation_metrics.json")
    print("Evaluation run finished.")


if __name__ == "__main__":
    main()
