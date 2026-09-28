# Flaky Test Pattern Analyzer

An end-to-end hackathon solution built for SDETs and QA teams to analyze repeated automated test records, calculate transparent flakiness scores, detect behavioral anomalies, and delegate pattern interpretation to a lightweight AI wrapper.

## Project Deliverables
1. **Ranked Flakiness Score Table:** Displays tests sorted by instability score and severity.
2. **Probable-Cause Tag per Flaky Test:** Uses deterministic pattern analysis backed by AI to tag failures as *Timing*, *Environment*, *Intermittent*, or *Ordering*.
3. **Overall Stability Summary:** High-level metrics and textual summary of suite health.

## Technology Stack
- **Python / Streamlit:** Interactive dashboard interface.
- **Pandas / NumPy:** Data validation, cleaning, aggregation, and scoring.
- **Plotly:** Visual distribution charts.
- **OpenAI API:** Single-task pattern interpretation.

## How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt