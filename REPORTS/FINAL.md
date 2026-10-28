# Final Pipeline Report: smollm3

## Executive Summary
The Canonical inference snap (`smollm3`) packaging SmolLM3-3B Q4_K_M GGUF for low-latency CPU-only inference on a System76 Gazelle laptop has been scaffolded, validated, packed, and benchmarked autonomously following Canonical's Inference Snap Maker SDK v2 specifications.

## Delivered Artifacts
The workspace `/home/cgegout/projects/smollm3` contains:
1. **Snap Packages**:
   - `smollm3_2.0.0-beta.18+9f606f5_amd64.snap` (SHA256: `995b3d4637f668e4f5bb028de6a4cbeef85df736b9f0c7be7c4360d4f37a5a4f`)
   - `smollm3+smollm3-3b-q4-k-m-gguf_2.0.0-beta.18+9f606f5.comp` (SHA256: `e5ad5eb782118a30606c66138c53b93733c5bd9e4fee6b2be7f756340b615949`)
   - `smollm3+llamacpp_2.0.0-beta.18+9f606f5.comp` (SHA256: `bda28b97238c46f033dfd294b489bfb087af222d176b715886f1ee5af35b42a0`)
   - `SHA256SUMS` tracking artifact hashes.
2. **Reproducible Source & Configuration**:
   - `snap/snapcraft.yaml`: Core24, strict confinement, pinned CLI v2.0.0-beta.18 and llama.cpp runtime b11669.
   - `engines/cpu/server`: Execution wrapper configured with CPU affinity (6 threads), prompt caching (`--cache-prompt`), idle retention (`--sleep-idle-seconds -1`), and reasoning suppression (`--reasoning off`, `--reasoning-budget 0`).
   - `snap/hooks/install` & `snap/hooks/post-refresh`: Seed default ports 8356 (API) and 8357 (WebUI).
   - `.github/workflows/`: CPU-only CI/CD pipeline, PR validation, lint checks, and testing workflows.
3. **Validation & Benchmarks**:
   - `benchmark.py`: Repeatable latency testing script.
   - `test_api.py`: Automated OpenAI-compatible API verification suite.
   - Stage reports in `REPORTS/01-structure.md`, `REPORTS/02-workflows.md`, `REPORTS/03-static-checks.md`, and `REPORTS/04-build-and-test.md`.
4. **Integration Guides**:
   - `MODEL_PROVENANCE.md`: Model card, SHA256 checksums, and Apache 2.0 attribution.
   - `HAL9000_INTEGRATION.md`: Endpoint configuration, cURL and Python code snippets for HAL 9000.

## Benchmark & Performance Summary
- **Target Hardware**: Intel Core 7 250H (14 cores / 20 threads: 6 P-cores, 8 E-cores).
- **Optimal Threading**: 6 threads (physical Performance cores).
- **Startup Time**: ~1.81 s
- **Average Response Latency**: 3.18 s for 128-token conversational turns.
- **Generation Speed**: ~9.1 – 11.3 tokens/sec.
- **Memory Footprint**: ~3.49 GB resident memory (RSS).
- **Reasoning Suppression**: Confirmed zero `<think>` token overhead.

## Precise Blocker & Status Separation
- **Verified Complete**: Structure generation, CI/CD workflows, static schema checks, artifact packaging, CPU tuning benchmark, and standalone OpenAI-compatible API acceptance tests.
- **Unverified (Requires Root Access)**: Local `snap install --dangerous` and `dev/smoke-test.sh` because non-interactive `sudo -n true` exited 1 (`sudo: interactive authentication is required`). Sudo was not retried or prompted, preserving live snaps and host state.
