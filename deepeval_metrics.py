
import os
import time

from dotenv import load_dotenv
from deepeval.models import GeminiModel
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    HallucinationMetric,
)
from deepeval.test_case import LLMTestCase

load_dotenv()


def evaluate_with_deepeval(question, answer, context=None):
    context = context or []

    if isinstance(context, str):
        context = [context]

    result = {
        "faithfulness": None,
        "answer_relevance": None,
        "hallucination": None,
        "status": "NOT RUN",
        "error": None,
    }

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        result["status"] = "ERROR"
        result["error"] = "GEMINI_API_KEY is missing from .env"
        return result

    try:
        judge_model = GeminiModel(
            model="gemini-3.8-flash",
            api_key=api_key,
            temperature=0,
        )

        test_case = LLMTestCase(
            input=question,
            actual_output=answer,
            retrieval_context=context,
            context=context,
        )

        metrics = [
            (
                "faithfulness",
                FaithfulnessMetric(
                    threshold=0.5,
                    model=judge_model,
                ),
            ),
            (
                "answer_relevance",
                AnswerRelevancyMetric(
                    threshold=0.5,
                    model=judge_model,
                ),
            ),
            (
                "hallucination",
                HallucinationMetric(
                    threshold=0.5,
                    model=judge_model,
                ),
            ),
        ]

        for key, metric in metrics:
            last_error = None

            for attempt in range(3):
                try:
                    metric.measure(test_case)

                    result[key] = {
                        "score": metric.score,
                        "passed": metric.is_successful(),
                        "reason": getattr(metric, "reason", None),
                    }

                    last_error = None
                    break

                except Exception as error:
                    last_error = error

                    if attempt < 2:
                        time.sleep(2 * (attempt + 1))

            if last_error is not None:
                result[key] = {
                    "score": None,
                    "passed": None,
                    "reason": None,
                    "error": str(last_error),
                }

        completed = [
            result[key]
            for key in (
                "faithfulness",
                "answer_relevance",
                "hallucination",
            )
            if isinstance(result[key], dict)
            and result[key].get("score") is not None
        ]

        if len(completed) == 3:
            result["status"] = "COMPLETED"
        elif completed:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "ERROR"

    except Exception as error:
        result["status"] = "ERROR"
        result["error"] = str(error)

    return result
