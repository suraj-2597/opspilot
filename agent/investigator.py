import json

import ollama

from agent.tools import (
    get_recent_logs,
    get_service_health,
    get_recent_deployments,
    search_knowledge,
)


SYSTEM_PROMPT = """
You are OpsPilot, an AI production incident investigator.

Your job is to investigate software incidents using evidence
collected from a simulated production environment.

Your analysis must be evidence-grounded.

Rules:

1. Identify the likely root cause.
2. Separate root causes from downstream symptoms.
3. Use concrete evidence from logs and metrics.
4. Use historical knowledge when relevant.
5. Check recent deployments when forming hypotheses.
6. Recommend practical remediation steps.
7. If evidence is insufficient, explicitly say so.
8. Never invent evidence.
9. Never invent logs, metrics, deployments, incidents, or timestamps.
10. Never infer service dependencies unless they are explicitly present
    in the evidence.
11. Never claim that one event happened before another unless the
    timestamps prove it.
12. Clearly distinguish observed facts from hypotheses.
13. Every root-cause claim must be supported by evidence.
14. Historical knowledge should support the investigation but must not
    be treated as proof of the current root cause.

Use the following structure:

Incident Summary
Severity
Likely Root Cause
Evidence
Historical Context
Recent Deployment Analysis
Recommended Actions
Confidence

For Confidence, provide a percentage and briefly explain why.
"""


def investigate(incident):

    print("\nCollecting production evidence...")

    logs = get_recent_logs(30)

    print("Checking service health...")

    health = get_service_health()

    print("Checking recent deployments...")

    deployments = get_recent_deployments(10)

    print("Searching historical knowledge...")

    knowledge = search_knowledge(
        incident,
        limit=3,
    )

    evidence = {
        "incident": incident,
        "recent_logs": logs,
        "service_health": health,
        "recent_deployments": deployments,
        "knowledge": knowledge,
    }

    prompt = f"""
Investigate this production incident:

{incident}

Below is the evidence collected from the production system.

========================
RECENT LOGS
========================

{json.dumps(logs, default=str, indent=2)}


========================
SERVICE HEALTH
========================

{json.dumps(health, default=str, indent=2)}


========================
RECENT DEPLOYMENTS
========================

{json.dumps(deployments, default=str, indent=2)}


========================
RELEVANT KNOWLEDGE
========================

{json.dumps(knowledge, default=str, indent=2)}


========================
INVESTIGATION TASK
========================

Determine:

1. What failed first according to the timestamps?
2. Which services are showing errors?
3. What evidence supports the likely root cause?
4. Which failures may be downstream symptoms?
5. Did a recent deployment potentially contribute?
6. Does historical knowledge support the hypothesis?
7. What should engineers investigate next?

IMPORTANT:

Do not invent relationships between services.

Do not invent events that are not present in the evidence.

If the evidence does not prove something, describe it as a hypothesis
rather than a fact.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":

    incident = input(
        "Describe the production incident: "
    )

    print("\n")
    print("=" * 70)
    print("OPSPILOT INVESTIGATION")
    print("=" * 70)

    result = investigate(incident)

    print()
    print(result)
