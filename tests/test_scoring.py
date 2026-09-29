import pandas as pd
from analyzer.scoring import calculate_metrics

#Verify correct calculation of basic test execution metrics.
def test_calculate_metrics():
    data = {
        'run_id': [1, 2, 3],
        'test_name': ['SampleTest', 'SampleTest', 'SampleTest'],
        'status': ['PASS', 'FAIL', 'PASS'],
        'timestamp': ['2026-09-01 09:00:00', '2026-09-01 09:05:00', '2026-09-01 09:10:00'],
        'environment': ['Chrome', 'Chrome', 'Chrome'],
        'duration': [1.0, 5.0, 1.1]
    }
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    result = calculate_metrics(df)
    assert not result.empty
    assert result.iloc[0]['test_name'] == 'SampleTest'
    assert result.iloc[0]['failures'] == 1
    assert result.iloc[0]['passes'] == 2

#Verify that tests with only PASS results receive a zero flakiness score.
def test_all_pass_score_is_zero():
    data = {
        'run_id': [1, 2, 3],
        'test_name': ['StableTest'] * 3,
        'status': ['PASS', 'PASS', 'PASS'],
        'timestamp': [
            '2026-09-01 09:00:00',
            '2026-09-01 09:05:00',
            '2026-09-01 09:10:00'
        ],
        'environment': ['Chrome'] * 3,
        'duration': [1.0, 1.1, 1.2]
    }

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    result = calculate_metrics(df)

    assert result.iloc[0]['score'] == 0

#Verify that tests with only FAIL results receive a zero flakiness score
def test_all_fail_score_is_zero():
    data = {
        'run_id': [1, 2, 3],
        'test_name': ['FailingTest'] * 3,
        'status': ['FAIL', 'FAIL', 'FAIL'],
        'timestamp': [
            '2026-09-01 09:00:00',
            '2026-09-01 09:05:00',
            '2026-09-01 09:10:00'
        ],
        'environment': ['Chrome'] * 3,
        'duration': [5.0, 5.2, 5.1]
    }

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    result = calculate_metrics(df)

    assert result.iloc[0]['score'] == 0

#Verify that alternating PASS and FAIL results are assigned a non zero flakiness score
def test_flaky_pattern_has_nonzero_score():
    data = {
        'run_id': [1, 2, 3, 4],
        'test_name': ['FlakyTest'] * 4,
        'status': ['PASS', 'FAIL', 'PASS', 'FAIL'],
        'timestamp': [
            '2026-09-01 09:00:00',
            '2026-09-01 09:05:00',
            '2026-09-01 09:10:00',
            '2026-09-01 09:15:00'
        ],
        'environment': ['Chrome'] * 4,
        'duration': [1.0, 5.0, 1.1, 5.2]
    }

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    result = calculate_metrics(df)

    assert result.iloc[0]['score'] > 0