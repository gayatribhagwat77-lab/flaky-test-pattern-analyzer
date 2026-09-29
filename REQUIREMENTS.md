# Flaky Test Pattern Analyzer

## 1. Project Overview

**Objective:** Analyze historical test-run data to identify potentially flaky tests and provide stability insights.

**Target Users:** QA Engineers, SDETs, and QA Leads.

**Value:** Helps teams identify unstable tests, prioritize investigation, and understand test-suite stability.

## 2. Functional Requirements

### Data Ingestion & Validation
- Accept test-run data in CSV format.
- Validate required fields and data.
- Display errors for invalid or missing data.

### Pattern Analysis
- Analyze PASS/FAIL execution patterns chronologically.
- Detect PASS → FAIL and FAIL → PASS transitions.
- Distinguish stable, consistently failing, and potentially flaky tests.

### Scoring & Ranking
- Calculate a deterministic flakiness score from 0–100.
- Rank tests based on their scores.

### Probable-Cause Classification
- Provide a probable cause for unstable tests.
- Use categories such as Timing, Environment, Ordering, or Intermittent.
- Treat the result as a probable cause, not a confirmed root cause.

### Dashboard
- Display stability summary.
- Display ranked test results and scores.
- Provide test-level details and visualizations.

## 3. Non-Functional Requirements

- **Performance:** Process the hackathon-sized dataset interactively.
- **Usability:** Provide clear results and validation messages.
- **Maintainability:** Keep validation, analysis, scoring, AI, and UI modular.
- **Security:** Do not hard-code or expose AI credentials.

## 4. Constraints & Assumptions

- **Tech Stack:** Python, Streamlit, Pandas, NumPy, Plotly, Pytest, CSV, Ollama.
- **Dataset:** Small hackathon-sized test-run dataset.
- **Assumption:** Each row represents a test execution.
- **Out of Scope:** Test execution, automatic test fixing, CI/CD integration, and definitive root-cause detection.

## 5. Acceptance Criteria

- Valid CSV data is accepted and analyzed.
- Invalid or incomplete data produces an appropriate error.
- All PASS → Stable with score 0.
- All FAIL → Consistently failing, not flaky.
- Mixed PASS/FAIL → Flakiness is analyzed and scored.
- Tests are ranked according to their scores.
- Dashboard displays the analysis results and stability summary.