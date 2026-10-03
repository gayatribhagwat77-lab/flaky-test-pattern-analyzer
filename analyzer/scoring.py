import pandas as pd
import numpy as np

def calculate_metrics(df):
    test_summaries = []
    
    for test_name, group in df.groupby('test_name'):
        total_runs = len(group)
        passes = len(group[group['status'] == 'PASS'])
        failures = len(group[group['status'] == 'FAIL'])
        failure_rate = failures / total_runs if total_runs > 0 else 0
        pass_rate = passes / total_runs if total_runs > 0 else 0
        
        statuses = group['status'].tolist()
        switches = sum(1 for i in range(1, len(statuses)) if statuses[i] != statuses[i-1])
        switch_rate = switches / (total_runs - 1) if total_runs > 1 else 0
        
        inconsistency = 1 - abs(pass_rate - failure_rate)
        
        # Calculate flakiness score
        if switches == 0:
            score = 0
        else:
            score = (0.4 * (failure_rate * 100)) + (0.4 * (switch_rate * 100)) + (0.2 * (inconsistency * 100))

        
        score = round(min(max(score, 0), 100), 2)
        
        if score >= 70:
            severity = "CRITICAL"
        elif score >= 40:
            severity = "HIGH"
        elif score >= 20:
            severity = "MEDIUM"
        else:
            severity = "LOW"
            
        pass_durations = group[group['status'] == 'PASS']['duration']
        fail_durations = group[group['status'] == 'FAIL']['duration']
        avg_pass_dur = pass_durations.mean() if not pass_durations.empty else 0.0
        avg_fail_dur = fail_durations.mean() if not fail_durations.empty else 0.0
        
        env_failures = (
            group.groupby('environment')['status']
            .value_counts()
            .unstack(fill_value=0)
            .to_dict('index')
        )        
        test_summaries.append({
            'test_name': test_name,
            'total_runs': total_runs,
            'passes': passes,
            'failures': failures,
            'failure_rate': round(failure_rate * 100, 1),
            'switches': switches,
            'score': score,
            'severity': severity,
            'pattern': " - ".join(statuses),
            'avg_pass_dur': round(avg_pass_dur, 2),
            'avg_fail_dur': round(avg_fail_dur, 2),
            'env_failures': env_failures
        })
        
    summary_df = pd.DataFrame(test_summaries)
    if not summary_df.empty:
        summary_df = summary_df.sort_values(by='score', ascending=False)
    return summary_df