"""Run the lab benchmark and write markdown plus local trace evidence."""

from pathlib import Path

from multi_agent_research_lab.evaluation.benchmark import (
    baseline_runner,
    load_queries,
    multi_agent_runner,
    run_benchmark,
)
from multi_agent_research_lab.evaluation.report import render_markdown_report
from multi_agent_research_lab.observability.tracing import export_trace


def main() -> None:
    report_dir = Path("reports")
    trace_dir = report_dir / "traces"
    metrics = []
    for index, query in enumerate(load_queries(), 1):
        for name, runner in (("baseline", baseline_runner), ("multi-agent", multi_agent_runner)):
            state, item = run_benchmark(f"{name}-{index}", query, runner)
            metrics.append(item)
            export_trace(state.trace, trace_dir / f"{name}-{index}.jsonl")
    (report_dir / "benchmark_report.md").write_text(
        render_markdown_report(metrics), encoding="utf-8"
    )
    print(f"Wrote {report_dir / 'benchmark_report.md'} and {len(metrics)} metric rows")


if __name__ == "__main__":
    main()
