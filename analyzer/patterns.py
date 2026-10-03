def extract_pattern_context(row):
    context = {
        "test": row['test_name'],
        "total_runs": row['total_runs'],
        "failures": row['failures'],
        "failure_rate": f"{row['failure_rate']}%",
        "pattern": row['pattern'],
        "avg_pass_duration": row['avg_pass_dur'],
        "avg_fail_duration": row['avg_fail_dur'],
        "environment_failures": row['env_failures']

    }
    return context