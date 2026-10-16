# LLM Evaluation & Guardrails — Task 04

## 1. Project Overview
This project provides a Flask dashboard to evaluate a supplied question and answer using basic quality checks, prompt-injection detection, and guardrail checks.

## 2. Implemented Features
- Flask-based evaluation dashboard.
- Eight basic evaluation checks.
- Basic word-overlap relevance signal.
- Local pattern-based prompt-injection and unsafe-input screening.
- JSONL evaluation logging.
- Evaluation latency measurement.
- Guardrails AI package import verified.

## 3. DeepEval Metrics
The project includes Faithfulness, Answer Relevance, and Hallucination metric configurations using Gemini as the judge model.

Status: NOT RUN successfully. Gemini returned HTTP 429 RESOURCE_EXHAUSTED because the free-tier API quota was exhausted. No metric scores have been fabricated.

## 4. Langfuse Tracing
The Langfuse SDK is installed, and the tracing helper imports successfully. End-to-end trace delivery has not been verified. The dashboard currently reports tracing as temporarily disabled.

## 5. Limitations
- The dashboard evaluates a supplied answer; it does not generate an LLM response.
- LLM token usage is unavailable.
- Pattern-based checks cannot detect every unsafe input or prompt injection.
- Word overlap does not guarantee factual accuracy.
- Live DeepEval metrics require available judge-model quota.

## 6. Test Results
- Flask app import: PASS.
- Guardrails AI package import: PASS.
- Prompt-injection pattern test: PASS.
- Basic dashboard evaluation: PASS in local testing.
- DeepEval live metrics: BLOCKED by API quota.
- Langfuse end-to-end tracing: NOT VERIFIED.

## 7. Conclusion
The basic evaluation dashboard is operational. DeepEval live metrics and Langfuse trace delivery remain incomplete and must be verified before claiming full integration.
