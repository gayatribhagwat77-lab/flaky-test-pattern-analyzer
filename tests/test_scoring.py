import pandas as pd
from analyzer.scoring import calculate_metrics

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