"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics, averages, traces, and failure analysis."""

    def average(prefix: str, field: str) -> float:
        values = [
            getattr(item, field)
            for item in metrics
            if item.run_name.startswith(prefix) and getattr(item, field) is not None
        ]
        return sum(values) / len(values) if values else 0.0

    lines = [
        "# Benchmark Report: Single-Agent vs Multi-Agent Research",
        "",
        "## Objective",
        "",
        "This benchmark compares a single-agent baseline with the "
        "Supervisor → Researcher → Analyst → Writer workflow.",
        "The multi-agent path uses the bundled offline research corpus.",
        "",
        "## Metrics",
        "",
        "Latency is wall-clock time; cost is provider-reported or estimated usage; "
        "quality is an implementation proxy; citation coverage measures source IDs "
        "in state; failure rate counts unsuccessful runs.",
        "",
        "## Results",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality | Citation cov. | Failure rate | Notes |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        citation = "" if item.citation_coverage is None else f"{item.citation_coverage:.0%}"
        failure = "" if item.failure_rate is None else f"{item.failure_rate:.0%}"
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} "
            f"| {citation} | {failure} | {item.notes} |"
        )
    for prefix, label in (("baseline", "Average baseline"), ("multi-agent", "Average multi-agent")):
        lines.append(
            f"| **{label}** | **{average(prefix, 'latency_seconds'):.2f}** | "
            f"**{average(prefix, 'estimated_cost_usd'):.4f}** | "
            f"**{average(prefix, 'quality_score'):.1f}** | "
            f"**{average(prefix, 'citation_coverage'):.0%}** | "
            f"**{average(prefix, 'failure_rate'):.0%}** | — |"
        )
    lines.extend(
        [
            "",
            "The latency comparison is not fully controlled: the baseline uses a "
            "remote LLM call, while the multi-agent worker path uses deterministic "
            "local retrieval and synthesis.",
            "",
            "## Failure-mode analysis",
            "",
            "The baseline is simpler but does not maintain a source ledger automatically, "
            "so unsupported claims are harder to diagnose. Multi-agent handoffs add failure "
            "surface area—search failure, malformed state, provenance loss, writer citation "
            "loss, or provider timeout—but each handoff is explicit and inspectable. "
            "Provider failures use a local fallback for demos; production should add bounded "
            "retry, alerting, and a degraded-output flag.",
            "",
            "## Trace evidence",
            "",
            "Local traces are exported as JSONL under `reports/traces/`. When configured, "
            "LangSmith receives named workflow-node traces.",
            "",
            "## Reproduction",
            "",
            "```powershell",
            ".\\.venv\\Scripts\\python.exe scripts/run_benchmark.py",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"
