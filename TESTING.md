# Testing: Flaky Test Pattern Analyzer

## 1. Test Environment

- Python 3.9
- Pytest


## 2. Test Scenarios
1. Valid CSV Upload
2. Invalid CSV Upload
3. Test Pattern and Classification
4. Multiple Test Analysis and Ranking
5. Probable-Cause Classification
6. Deep Dive Analysis
7. Limited Execution History
---

## 3. Test Cases

### TC01 – Valid CSV Upload

**Test Steps:**
1. Open the application.
2. Upload a valid CSV file.
3. Run the analysis.
4. Observe the results.

**Expected Result:**  
The CSV is accepted and analysis results are displayed.

**Status:** Passed

---

### TC02 – Missing Required Column

**Test Steps:**
1. Prepare a CSV with a required column missing.
2. Upload the CSV.
3. Observe the validation result.

**Expected Result:**  
The application rejects the CSV and displays an appropriate validation error.

**Status:** Passed

---

### TC03 – Invalid Status

**Test Steps:**
1. Prepare a CSV containing an invalid status value.
2. Upload the CSV.
3. Observe the validation result.

**Expected Result:**  
The invalid status is detected and an appropriate validation error is displayed.

**Status:** Passed

---
### TC04 – Invalid Timestamp

**Test Steps:**
1. Prepare a CSV containing an invalid timestamp.
2. Upload the CSV.
3. Observe the validation result.

**Expected Result:**  
An appropriate timestamp validation error is displayed.

**Status:** Passed

---

### TC05 – Stable Test Pattern

**Test Steps:**
1. Prepare test data with all executions having PASS status.
2. Upload the CSV.
3. Run the analysis.
4. Check the test result.

**Expected Result:**  
The test is identified as stable with a flakiness score of 0.

**Status:** Passed

---

### TC06 – Consistently Failing Test

**Test Steps:**
1. Prepare test data with all executions having FAIL status.
2. Upload the CSV.
3. Run the analysis.
4. Check the test result.

**Expected Result:**  
The test is identified as consistently failing and has a flakiness score of 0.

**Status:** Passed

---

### TC07 – Flaky Test Identification

**Test Steps:**
1. Prepare test data with changing PASS/FAIL results.
2. Upload the CSV.
3. Run the analysis.
4. Check the test result.

**Expected Result:**  
The test is identified as a flaky candidate and receives a non-zero flakiness score.

**Status:** Passed

---

### TC08 – Multiple Test Names

**Test Steps:**
1. Prepare a CSV containing multiple test names and executions.
2. Upload the CSV.
3. Run the analysis.
4. Check the results.

**Expected Result:**  
Each test is analysed separately with its own metrics and score.

**Status:** Passed

---

### TC09 – Environment-Specific Failures

**Test Steps:**
1. Prepare test data with failures associated with a particular environment.
2. Upload the CSV.
3. Run the analysis.
4. Check the probable-cause information.

**Expected Result:**  
Environment information is available for probable-cause analysis.

**Status:** Passed

---

### TC10 – Test Selection in Deep Dive

**Test Steps:**
1. Upload a valid CSV containing multiple tests.
2. Run the analysis.
3. Open the Deep Dive section.
4. Select a test and view its details.

**Expected Result:**  
Detailed information for the selected test is displayed.

**Status:** Passed

---

### TC11 – Single Execution

**Test Steps:**
1. Prepare a CSV containing one test execution.
2. Upload the CSV.
3. Run the analysis.
4. Check the result.

**Expected Result:**  
The system processes the record without crashing or incorrectly identifying it as flaky.

**Status:** Passed

---

### TC12 – Two Executions

**Test Steps:**
1. Prepare two executions with PASS and FAIL results.
2. Upload the CSV.
3. Run the analysis.
4. Check the transition and score.

**Expected Result:**  
The PASS/FAIL transition is detected and the system handles the limited execution history without crashing.

**Status:** Passed

## 4. Unit Tests
### `tests/test_scoring.py`

The scoring test module contains four tests:

- **`test_calculate_metrics`**  
  Verifies the basic calculation of test execution metrics.

- **`test_all_pass_score_is_zero`**  
  Verifies that a test with only PASS results receives a flakiness score of `0`.

- **`test_all_fail_score_is_zero`**  
  Verifies that a test with only FAIL results receives a flakiness score of `0`.

- **`test_flaky_pattern_has_nonzero_score`**  
  Verifies that a mixed PASS/FAIL pattern receives a non-zero flakiness score.

### `tests/test_preprocessing.py`

- **`test_valid_csv_input`**  
  Verifies that valid CSV input is accepted and processed correctly.

### Running Unit Tests

```bash
python -m pytest
```

### Test Result

The scoring unit tests were executed successfully.

---

