# Benchmark Report: Single-Agent vs Multi-Agent Research

## Objective

This benchmark compares a single-agent baseline with the Supervisor → Researcher → Analyst → Writer workflow.
The multi-agent path uses the bundled offline research corpus.

## Metrics

Latency is wall-clock time; cost is provider-reported or estimated usage; quality is an implementation proxy; citation coverage measures source IDs in state; failure rate counts unsuccessful runs.

## Results

| Run | Latency (s) | Cost (USD) | Quality | Citation cov. | Failure rate | Notes |
|---|---:|---:|---:|---:|---:|---|
| baseline-1 | 4.25 | 0.0011 | 6.0 | 0% | 0% | routes=[]; error=none |
| multi-agent-1 | 0.57 |  | 10.0 | 100% | 0% | routes=['researcher', 'analyst', 'writer']; error=none |
| baseline-2 | 2.41 | 0.0012 | 6.0 | 0% | 0% | routes=[]; error=none |
| multi-agent-2 | 0.10 |  | 10.0 | 100% | 0% | routes=['researcher', 'analyst', 'writer']; error=none |
| baseline-3 | 2.16 | 0.0011 | 6.0 | 0% | 0% | routes=[]; error=none |
| multi-agent-3 | 0.10 |  | 10.0 | 100% | 0% | routes=['researcher', 'analyst', 'writer']; error=none |
| **Average baseline** | **2.94** | **0.0011** | **6.0** | **0%** | **0%** | — |
| **Average multi-agent** | **0.25** | **0.0000** | **10.0** | **100%** | **0%** | — |

The latency comparison is not fully controlled: the baseline uses a remote LLM call, while the multi-agent worker path uses deterministic local retrieval and synthesis.

## Failure-mode analysis

The baseline is simpler but does not maintain a source ledger automatically, so unsupported claims are harder to diagnose. Multi-agent handoffs add failure surface area—search failure, malformed state, provenance loss, writer citation loss, or provider timeout—but each handoff is explicit and inspectable. Provider failures use a local fallback for demos; production should add bounded retry, alerting, and a degraded-output flag.

## Trace evidence

Local traces are exported as JSONL under `reports/traces/`. When configured, LangSmith receives named workflow-node traces.

### Public LangSmith trace

[Open public LangSmith supervisor](https://smith.langchain.com/public/9e93002b-e8ab-45e7-866d-7f92f93e66ae/r/01a01e46-b6ec-7273-aa7e-1226d216f323?start_time=2026-08-20T08%3A25%3A45.964611Z)

[Open public LangSmith analyst](https://smith.langchain.com/public/b77ae467-76d0-4bdc-bab6-c1038db8cda0/r/01a01e46-b6eb-7760-921b-733a320e6309?start_time=2026-08-20T08%3A25%3A45.963608Z)

[Open the public LangSmith writer](https://smith.langchain.com/public/430c1962-5e8e-44a7-803a-6554b48f8552/r/01a01e46-b6ec-70a1-8b07-31f6cde2759f?start_time=2026-08-20T08%3A25%3A45.964611Z)

## Reproduction

```powershell
.\.venv\Scripts\python.exe scripts/run_benchmark.py
```
