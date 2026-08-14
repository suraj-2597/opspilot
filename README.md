# OpsPilot 🚀

## AI-Powered Production Incident Investigation Platform

OpsPilot is an AI-assisted SRE/DevOps platform designed to help engineers
investigate production incidents faster.

When a production incident occurs, engineers often need to manually correlate
information across logs, services, deployments, databases, historical incidents,
and operational runbooks.

OpsPilot brings these sources together and uses AI + RAG to produce a structured
incident investigation with:

- Incident summary
- Severity assessment
- Likely root cause
- Supporting evidence
- Historical context
- Recent deployment analysis
- Recommended remediation actions
- Confidence score

The goal is not to replace engineers.

The goal is to reduce the amount of time engineers spend collecting and
correlating production evidence so they can focus on solving the problem.

---

# Why OpsPilot?

Imagine an e-commerce company experiences:

> "Checkout requests are failing and the Order Service is experiencing
> database timeouts."

Normally, an engineer may need to:

1. Check the Checkout Service.
2. Check the Order Service.
3. Inspect database metrics.
4. Look through application logs.
5. Check recent deployments.
6. Search previous incidents.
7. Read operational runbooks.
8. Correlate timestamps.
9. Determine the likely root cause.
10. Decide what remediation steps to take.

This process can take significant time during a production outage.

OpsPilot automates much of the investigation and presents the evidence in a
single investigation report.

---

# How It Works

```text
                  Production Incident
                         │
                         ▼
                ┌─────────────────┐
                │  React Frontend │
                │ OpsPilot Console│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  FastAPI API    │
                └────────┬────────┘
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
        ┌─────────┐ ┌─────────┐ ┌────────────┐
        │ Service │ │Postgres │ │ RAG /      │
        │ Evidence│ │   DB    │ │ Knowledge  │
        └────┬────┘ └────┬────┘ └─────┬──────┘
             │           │            │
             └───────────┼────────────┘
                         ▼
                  ┌─────────────┐
                  │     LLM     │
                  │ Ollama /    │
                  │ OpenAI      │
                  └──────┬──────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Investigation   │
                │ Report          │
                └─────────────────┘
