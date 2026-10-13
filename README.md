\# LLM Evaluation \& Guardrails



A Python Flask web application that evaluates LLM responses using basic rule-based checks and records evaluation results.



\## Features



\- Evaluate question and response inputs

\- Check for empty questions and answers

\- Check response length

\- Calculate a basic word-overlap relevance signal

\- Flag selected potentially unsafe phrases

\- Detect selected prompt-injection phrases

\- Calculate an evaluation score

\- Save results as JSON Lines logs

\- Provide a health-check endpoint



\## Technologies Used



\- Python

\- Flask

\- HTML and CSS

\- JSON



\## Installation



1\. Clone or download this repository.

2\. Create a virtual environment:



&#x20;  ```bash

&#x20;  python -m venv venv

&#x20;  ```



3\. Install dependencies:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



\## Run the Application



```bash

python app.py

```



Open this address in your browser:



http://127.0.0.1:5000



\## How to Use



1\. Enter a question or prompt.

2\. Enter the LLM response you want to evaluate.

3\. Click \*\*Evaluate Response\*\*.

4\. Review the checks, score, and review note.

5\. Evaluation records are saved in `evaluation\_logs.jsonl`.



\## Health Check



Visit `/health` to check whether the Flask application is running.



\## Limitations



This project uses basic rule-based checks. Word overlap does not reliably measure semantic relevance. Keyword-based guardrails can miss unsafe content or flag harmless text. The score is not a measure of factual accuracy, and the application does not independently verify claims or guarantee safety.



This project is a learning prototype, not a production-grade LLM evaluation or security system.

