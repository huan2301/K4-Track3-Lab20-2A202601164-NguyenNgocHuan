"""Benchmark runners for single-agent vs multi-agent."""

import json
from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import Any

from multi_agent_research_lab.core.schemas import BenchmarkMetrics, ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.services.llm_client import LLMClient

Runner = Callable[[str], ResearchState]


def run_benchmark(
    run_name: str, query: str, runner: Runner
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency, cost proxy, quality proxy, citations, and failures."""

    started = perf_counter()
    error = ""
    try:
        state = runner(query)
    except Exception as exc:
        state = ResearchState(request=ResearchQuery(query=query))
        state.errors.append(str(exc))
        error = type(exc).__name__
    latency = perf_counter() - started
    citation_count = sum(
        1 for source in state.sources if source.metadata.get("source_id")
    )
    has_answer = bool(state.final_answer)
    quality = 10.0 if has_answer and citation_count else 6.0 if has_answer else 0.0
    usage: dict[str, Any] = next(
        (event["payload"] for event in state.trace if event.get("name") == "baseline"),
        {},
    )
    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=usage.get("cost_usd"),
        quality_score=quality,
        citation_coverage=min(1.0, citation_count / 3) if has_answer else 0.0,
        failure_rate=0.0 if has_answer and not error else 1.0,
        notes=f"routes={state.route_history}; error={error or 'none'}",
    )
    return state, metrics


def baseline_runner(query: str) -> ResearchState:
    """Run one LLM baseline and keep usage in state trace."""
    started = perf_counter()
    response = LLMClient().complete(
        "You are a concise research assistant. State limitations and cite sources when supplied.",
        query,
    )
    state = ResearchState(request=ResearchQuery(query=query), final_answer=response.content)
    state.add_trace_event(
        "baseline",
        {
            "latency_seconds": perf_counter() - started,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "cost_usd": response.cost_usd,
        },
    )
    return state


def multi_agent_runner(query: str) -> ResearchState:
    """Run the compiled multi-agent workflow."""
    return MultiAgentWorkflow().run(ResearchState(request=ResearchQuery(query=query)))


def load_queries(path: Path | None = None) -> list[str]:
    """Load JSONL queries, otherwise derive queries from the offline corpus."""
    if path and path.exists():
        queries: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                item = json.loads(line)
                queries.append(item if isinstance(item, str) else item["query"])
        return queries
    corpus_queries: list[str] = []
    for topic_path in sorted(Path("ai_agent_offline_research_corpus_v2/topics").glob("*.json")):
        try:
            topic = json.loads(topic_path.read_text(encoding="utf-8")).get("topic", {})
        except (OSError, json.JSONDecodeError):
            continue
        question = topic.get("research_question")
        if question:
            corpus_queries.append(f"{question} Provide an evidence-based summary with citations.")
    if corpus_queries:
        return corpus_queries[:3]
    return [
        "Research GraphRAG state-of-the-art and write a 500-word summary",
        "Compare single-agent and multi-agent workflows for customer support",
        "Summarize production guardrails for LLM agents",
    ]
