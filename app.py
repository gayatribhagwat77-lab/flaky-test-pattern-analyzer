import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer.preprocessing import load_and_validate_data
from analyzer.scoring import calculate_metrics
from analyzer.patterns import extract_pattern_context
from analyzer.cause_classifier import classify_cause_with_ai

# Page configuration
st.set_page_config(
    page_title="Flaky Test Pattern Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    /* Enterprise Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.8rem !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 1.75rem !important;
        font-weight: 600;
    }
 section[data-testid="stSidebar"] hr {
        border-color: #f8fafc;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }
    [data-testid="stAppDeployButton"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer {
        display: none !important;
}
    [data-testid="stElementToolbar"] {
    display: none !important;
}
    
    
    /* Typography & Headers */
    h1 {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.85rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.2rem !important;
        letter-spacing: -0.01em;
        border-bottom: none;
        padding-bottom: 0.4rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1rem !important;
    }

    p {
        color: #475569;
        font-size: 0.95rem;
    }

    /* Sidebar Styling for Enterprise Dark Contrast */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
        color: #f8fafc !important;
        font-size: 0.95rem !important;
}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"],
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] small,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] span,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] div {
        color: #f8fafc !important;
}
    section[data-testid="stSidebar"] h2 {
        color: #f8fafc !important;
        border-bottom: none !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #f8fafc;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("Flaky Test Pattern Analyzer")
st.markdown("Enterprise telemetry and stability diagnostics for automated test suites.")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload Test Run CSV", type=["csv"])
st.sidebar.markdown("---")
use_sample = st.sidebar.checkbox("Use Built-in Sample Dataset.", value=True)

df = None
error = None

if uploaded_file is not None:
    df, error = load_and_validate_data(uploaded_file)
elif use_sample:
    df, error = load_and_validate_data("data/test_runs.csv")

if error:
    st.error(error)

elif df is not None:
        if df.empty:
            st.error("The uploaded CSV is empty. Please provide test-run records.")
        else:
            metrics_df = calculate_metrics(df)

            # Section 1:Overall Summary Metrics
            st.header("Overall Test Stability Summary")
            total_tests = len(metrics_df)
            
            flaky_tests = len(
                metrics_df[
                    (metrics_df['score'] >= 40) &
                    (metrics_df['passes'] > 0) &
                    (metrics_df['failures'] > 0)
                ]
            )
            stable_tests = len(
                metrics_df[
                    (metrics_df['passes'] == metrics_df['total_runs']) &
                    (metrics_df['failures'] == 0)
                ]
            )
            consistently_failing_tests = len(
                metrics_df[
                    (metrics_df['failures'] == metrics_df['total_runs']) &
                    (metrics_df['passes'] == 0)
                ]
            )
            avg_score = metrics_df['score'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Unique Tests", total_tests)
            col2.metric("Stable Tests", stable_tests)
            col3.metric("Flaky/Unstable Tests", flaky_tests)
            col4.metric("Avg Stability Risk Score", f"{round(avg_score, 1)}/100")
            
            # Textual stability pattern summary
            unstable_names = metrics_df[
                (metrics_df['score'] >= 40) &
                (metrics_df['passes'] > 0) &
                (metrics_df['failures'] > 0)
            ]['test_name'].tolist()
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            if flaky_tests > 0:
                st.info(f"**Stability Pattern Summary:** {flaky_tests} out of {total_tests} test cases exhibit flaky behavior ({', '.join(unstable_names)}). Failures correlate strongly with environment variations or execution duration anomalies.")
            else:
                st.success("**Stability Pattern Summary:** All test cases are currently stable with consistent outcomes.")

            # Section2:Score Table
            st.header("Ranked Flakiness Score Table")
            st.markdown("Detailed breakdown ordered by computed flakiness severity and core failure metrics.")
            st.dataframe(
                metrics_df[
                    [
                        'test_name',
                        'total_runs',
                        'passes',
                        'failures',
                        'failure_rate',
                        'switches',
                        'score',
                        'severity'
                    ]
                ],
                column_config={
                    "test_name": "Test Name",
                    "total_runs": "Total Runs",
                    "passes": "Passes",
                    "failures": "Failures",
                    "failure_rate": "Failure Rate",
                    "switches": "Switches",
                    "score": "Flakiness Score",
                    "severity": "Severity"
                },
                hide_index=True,
                use_container_width=True
            )
            # Section 3:Detailed Pattern & AI Probable-Cause Deep Dive 
            st.header("Detailed Pattern & AI Probable-Cause Deep Dive")

            selected_test = st.selectbox(
                "Select a Test Case for Probable-Cause Analysis",
                metrics_df['test_name'].tolist()
            )

            if selected_test:
                row = metrics_df[metrics_df['test_name'] == selected_test].iloc[0]
                context = extract_pattern_context(row)

                c1, c2 = st.columns([1, 1], gap="large")

                with c1:
                    st.subheader("Execution Pattern Metrics")
                    st.code(context['pattern'], language="text")
                    st.metric("Failure Rate", context['failure_rate'])
                    st.write(f"**Avg Pass Duration:** {context['avg_pass_duration']}s")
                    st.write(f"**Avg Fail Duration:** {context['avg_fail_duration']}s")
                    

                with c2:
                    st.subheader("AI Probable-Cause Tag")

                    if row['passes'] == row['total_runs']:
                        ai_output = (
                            "Cause: Not Applicable. \n"
                            "Confidence: 100%. \n"
                            "Explanation: The test passed in all executions and shows stable behavior."
                        )
                    elif row['failures'] == row['total_runs']:
                        ai_output = (
                            "Cause: Not Applicable. \n"
                            "Confidence: 100%. \n"
                            "Explanation: The test failed in all executions and shows consistent failure rather than flaky behavior."
                        )
                    else:
                        with st.spinner("Analyzing execution traces with AI..."):
                            ai_output = classify_cause_with_ai(context)

                    st.info(ai_output)
                    
            # Section 4:Chart
            st.header("Flakiness Distribution Chart")
            fig = px.bar(
                metrics_df,
                x='test_name',
                y='score',
                color='severity',
                title="Flakiness Risk Score by Test Case",
                color_discrete_map={
                    "CRITICAL": "#0f172a",
                    "HIGH": "#334155",
                    "MEDIUM": "#64748b",
                    "LOW": "#cbd5e1"
                },
                template="plotly_white"
            )
            fig.update_layout(
                xaxis_title="Test Name",
                yaxis_title="Risk Score",
                margin=dict(t=40, b=40, l=40, r=40),
                font=dict(
                    family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto",
                    size=12
                ),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff"
            )
            st.plotly_chart(fig, use_container_width=True)