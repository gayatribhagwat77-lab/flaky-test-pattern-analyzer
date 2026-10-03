from ollama import chat


def classify_cause_with_ai(context):

    prompt = f"""
Analyze this automated test execution data:

{context}

Choose ONE probable cause:
Timing
Environment
Ordering
Intermittent
Not Applicable

Return ONLY these 3 lines. Do not add anything else:

Cause: [one cause]
Confidence: [XX]%
Explanation: [maximum 10 words]

Rules:
- Alternating PASS/FAIL alone does NOT prove Ordering.
- Longer failure duration suggests Timing.
- Failures isolated to one environment suggest Environment.
- If the chosen cause is Environment, mention the specific environment name
  from the provided data.
- Use Ordering only when execution-order dependency is supported.
- Use Ordering only when the test's PASS/FAIL result is associated with
  a specific execution order or preceding test, and the result changes
  when that order changes.
- Do not classify as Ordering based only on an alternating PASS/FAIL pattern.
- Use Intermittent when no stronger cause is supported.
- This is a probable cause, not a confirmed root cause.
"""

    try:
        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return (
            "Cause: AI unavailable \n"
            f"Explanation: Unable to connect to the local AI model. {str(e)}"
        )