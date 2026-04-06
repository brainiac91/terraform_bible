# 26. SRE & Observability Practices

"You cannot manage what you cannot measure."

Site Reliability Engineering (SRE), pioneered by Google, bridges the gap between software development and systems operations. Observability is the cornerstone of SRE. Without comprehensive observability, deploying Kubernetes at scale is like flying blind into a storm.

## The Three Pillars of Observability
A robust observability stack relies on three distinct types of telemetry:

1. **Metrics**: Numerical representations of data measured over time (e.g., CPU %, HTTP 500 counts). Easily compressible and cheap to store.
2. **Logs**: Immutable, timestamped records of discrete events (e.g., Application traces, Nginx access logs). Highly detailed, but expensive to store at scale.
3. **Traces**: A representation of a single user's journey through a complex distributed system (e.g., tracking a single checkout request as it bounces between the Frontend, the Cart API, and the PostgreSQL database).

## The Prometheus Stack (Metrics)
In the Cloud Native ecosystem, **Prometheus** is the undisputed king of metrics. It utilizes a powerful pull-model architecture.

Unlike traditional agents (like Datadog) that push metrics outward to a central server, Prometheus reaches out to `/metrics` endpoints across your entire cluster and pulls the data in.

### PromQL
Prometheus stores data in a Time-Series Database (TSDB). You query it using PromQL:

```promql
# Find the per-second rate of total HTTP 500 errors over the last 5 minutes
rate(http_requests_total{status="500"}[5m])
```

## AlertManager & Symptom-Based Alerting
Legacy sysadmins set alerts on causes: *"Alert me if CPU goes over 90%."* This leads to **Alert Fatigue**. The CPU might be 95% because an optimized batch job is running perfectly.

SREs implement **Symptom-Based Alerting**. You only page a human if the user experience is impacted.
*   **Bad Alert**: Database CPU is at 99%.
*   **Good Alert**: Website load time exceeds 2 seconds for the 99th percentile of users (P99).

When symptom-based metrics breach thresholds, Prometheus forwards the event to `AlertManager`, which routes the critical alerts to PagerDuty or Slack.

## SLIs, SLOs, and Error Budgets
SREs govern system health through a structured mathematical framework:

*   **SLI (Service Level Indicator)**: What you are physically measuring. *(e.g., "The percentage of HTTP GET requests that return a 200 OK within 300ms")*
*   **SLO (Service Level Objective)**: The target you promise. *(e.g., "99.9% of requests over a rolling 30-day window will meet the SLI.")*

### The Error Budget
If your SLO is 99.9%, it means you are allowed 0.1% failure. This 0.1% is your **Error Budget**.
*   If your system is stable (budget intact), developers can ship rapid, risky features.
*   If your budget is depleted (you dropped below 99.9%), **all feature development freezes**. The team must focus exclusively on reliability until the budget recovers.

## Key Takeaway
Observability is not just dashboarding; it is the mathematical foundation of engineering velocity. By defining strict SLOs, you replace emotional arguments about stability ("We shouldn't deploy today, it feels risky") with data-driven engineering decisions.
