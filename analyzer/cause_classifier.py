from ollama import chat


def classify_cause_with_ai(context):

    prompt = f"""
    You are analyzing an automated software test for flakiness.

    Analyze the following execution data:

    {context}

    Your task is ONLY to assign a probable cause for the observed flaky behavior.

    Choose exactly ONE:
    - Timing
    - Environment
    - Ordering
    - Intermittent

    Use the available evidence:
    1. PASS/FAIL execution pattern
    2. Failure rate
    3. Average pass duration
    4. Average fail duration
    5. Environment failure information

    Important rules:
    - Alternating PASS/FAIL indicates flaky behavior, but does NOT by itself prove Ordering.
    - If failed executions take significantly longer than successful executions, consider Timing.
    - If failures are isolated to a particular environment, consider Environment.
    - Use Ordering only when the provided evidence specifically suggests execution-order dependency.
    - Use Intermittent when there is mixed behavior but no stronger evidence for Timing, Environment, or Ordering.
    - This is a probable cause, NOT a confirmed root cause.
    - Do not invent evidence that is not present in the data.
    - If the test has all PASS or all FAIL results, return Not Applicable.

    Return exactly:

    Cause: [Timing/Environment/Ordering/Intermittent/Not Applicable]
    Confidence: [XX]%
    Explanation: [1-2 short sentences based only on the provided data]
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