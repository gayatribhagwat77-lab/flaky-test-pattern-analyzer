import ollama


def classify_cause_with_ai(context):

    prompt = f"""
You are an AI test-analysis expert.

Analyze ONLY the test execution evidence provided below.

TEST DATA:
{context}

Your task is to select ONE probable cause.

Allowed causes:
- Timing
- Environment
- Ordering
- Unknown

Evaluate the evidence for ALL THREE causes before selecting one.

TIMING EVIDENCE:
Compare avg_pass_duration and avg_fail_duration.
Timing is supported when failed executions are substantially slower than
successful executions.
A small difference between pass and fail duration is weak evidence.

ENVIRONMENT EVIDENCE:
Examine environment_failures.
Environment is supported when failures are concentrated in an environment
while successful executions are present in another environment.
The presence of an environment name alone is NOT evidence.

ORDERING EVIDENCE:
Ordering is supported ONLY when the provided data contains evidence that the
result depends on execution order or a preceding test.
PASS/FAIL alternation alone is NOT ordering evidence.

Unknown:
Choose Unknown when the provided execution data does not contain enough
evidence to confidently support Timing, Environment, or Ordering.
Do not force a cause when the evidence is ambiguous.

DECISION:
Compare all available evidence.
Choose the cause with the strongest direct evidence.
Do NOT select a cause simply because it appears earlier in this prompt.
Do NOT invent missing evidence.
Do NOT treat weak evidence as strong evidence.

IMPORTANT EXAMPLES:

If:
avg_pass_duration = 3.10
avg_fail_duration = 3.22

This is only a small duration difference and should NOT by itself support Timing.

If:
avg_pass_duration = 2.85
avg_fail_duration = 11.75

This is strong evidence for Timing.

If:
Chrome = PASS 0, FAIL 2
Firefox = PASS 3, FAIL 0

This supports Environment.

If there is no explicit preceding-test or execution-order information,
do NOT claim Ordering.

This is a probable cause, not a confirmed root cause.

Return ONLY:

Cause: Timing
OR
Cause: Environment
OR
Cause: Ordering

Confidence: XX%
Explanation: maximum 10 words
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0,
                "seed": 42,
                "num_predict": 30,
                "top_k": 1,
                "top_p": 0.1
            },
            keep_alive="10m"
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return (
            "Cause: AI unavailable\n"
            "Confidence: 0%\n"
            f"Explanation: Unable to connect to local AI model. {str(e)}"
        )