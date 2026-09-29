import pandas as pd
from io import StringIO
from analyzer.preprocessing import load_and_validate_data

#Verify that valid testrun data is accepted and processed correctly
def test_valid_csv_input():
    csv_data = StringIO(
        """run_id,test_name,status,timestamp,environment,duration
            1,LoginTest,PASS,2026-09-01 09:00:00,Chrome,1.2
            2,LoginTest,FAIL,2026-09-01 09:05:00,Chrome,5.0
        """
    )

    result, error = load_and_validate_data(csv_data)

    assert error is None
    assert result is not None
    assert len(result) == 2