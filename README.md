# Flaky Test Pattern Analyzer

An end-to-end hackathon solution built for SDETs and QA teams to analyze repeated test records, calculate transparent flakiness scores, identify unstable test patterns, and provide probable-cause insights using AI.

## Project Deliverables

1. **Ranked Flakiness Score Table:** Displays tests sorted by flakiness score and severity.

2. **Probable-Cause Tag per Flaky Test:** Uses pattern analysis and AI to provide probable causes such as Timing, Environment, Intermittent, or Ordering.

3. **Overall Stability Summary:** Provides high-level metrics and a summary of test-suite stability.

## Technology Stack

- **Python / Streamlit:** Application and dashboard interface.
- **Pandas :** Data validation, processing, aggregation, and scoring.
- **Plotly:** Data visualization.
- **Ollama / Llama 3.2:** Probable-cause interpretation.
- **Pytest:** Unit testing of analysis logic.

## Input Data

The application accepts CSV test-run records containing fields such as:

- `run_id`
- `test_name`
- `status`
- `timestamp`
- `environment`
- `duration`

## How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the application

```bash
streamlit run app.py
```

### 3. Run tests

```bash
pytest
```
