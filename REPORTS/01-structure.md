# Stage 1: Inference Snap Structure Report

Target Workspace: `/home/cgegout/projects/hal9000-smollm3-snap`
Snap Name: `hal9000-smollm3`
Snap Title: `HAL9000 SmolLM3`
Architecture: `amd64` (and `arm64` cross-platform config)
Model ID: `smollm3-3b-q4-k-m-gguf`
Engine: `cpu`
Runtime: `llamacpp` (Canonical llama.cpp CPU build b11669)

## Structural Decisions
- **Variant Selection**: Variant A (single-model component). Model payload is ~1.82 GB (SmolLM3-3B-Q4_K_M.gguf), well within the single-component threshold (< 5 GB).
- **Model Payload**: Verified instruction-tuned SmolLM3-3B Q4_K_M GGUF (`sha256: 4de907d2d388a5508fb7cb443a06effe14cce3518b0a78d3bdd9e74d9edce989`).
- **Ports & Bindings**:
  - API HTTP port: `8356` (verified free on loopback)
  - Web UI HTTP port: `8357` (verified free on loopback)
  - Host binding: `127.0.0.1` (loopback-only)
- **Engine Tuning**:
  - CPU-only execution with AVX2/AVX-VNNI support.
  - Initial configuration: 6 CPU threads (matching physical P-cores on Intel Core 7 250H).
  - Context size fixed to 4096 tokens (`--ctx-size 4096`).
  - Slots: 1 (`--parallel 1`).
  - Thinking generation disabled via `--reasoning off --reasoning-budget 0`.
  - Idle unloading disabled via `--sleep-idle-seconds -1`.

## File Map
- **Scaffolded/Created**:
  - `snap/snapcraft.yaml`: Core24 snap specification pinning CLI v2.0.0-beta.18, WebUI v1.1.1, and llama.cpp b11669.
  - `snap/hooks/install`: Non-interactive install hook seeding ports 8356/8357 and falling back to cpu.
  - `snap/hooks/post-refresh`: Post-refresh hook refreshing active cpu engine.
  - `engines/cpu/engine.yaml`: Engine descriptor for cpu backend.
  - `engines/cpu/server`: Executable engine server invoking `llama-server`.
  - `models/smollm3-3b-q4-k-m-gguf/model.yaml`: Model descriptor specifying disk-size 1827M and text capability.
  - `runtimes/llamacpp/runtime.yaml`: Runtime descriptor with openai /v1 server and library search paths.
  - `scripts/server.sh`: Main daemon launcher.
  - `scripts/server-webui.sh`: Web UI daemon launcher.
  - `Makefile`: Project tasks including repeatable model preparation and dev submodule management.
  - `prepare_model.sh`: Repeatable offline model preparation wrapper.
  - `README.md`: Project documentation with YAML frontmatter.
  - `NOTICE`, `LICENSE`, `LICENSE-hal9000-smollm3`: Licensing and legal attributions.
  - `dev/`: Initialized Git submodule tracking `v2` of `canonical/inference-snaps-dev`.

```pipeline-report
target_workspace: /home/cgegout/projects/hal9000-smollm3-snap
snap_name: hal9000-smollm3
file_map:
  copied:
    - LICENSE
    - snap/gui/icon-256.png
  adapted:
    - snap/snapcraft.yaml — tailored for cpu-only hal9000-smollm3 with single model component
    - snap/hooks/install — seeded ports 8356/8357 with --fallback=cpu
    - snap/hooks/post-refresh — refresh cpu engine
    - engines/cpu/engine.yaml — cpu device constraints and smollm3-3b-q4-k-m-gguf model default
    - engines/cpu/server — llama-server with --reasoning off, --ctx-size 4096, --threads 6
    - models/smollm3-3b-q4-k-m-gguf/model.yaml — descriptor for 1827M SmolLM3-3B Q4_K_M GGUF
    - runtimes/llamacpp/runtime.yaml — llamacpp CPU runtime descriptor
    - scripts/server.sh — engine server launcher
    - scripts/server-webui.sh — WebUI server launcher
    - Makefile — offline model preparation and build targets
naming_decisions:
  - Snap name: hal9000-smollm3
  - Model ID: smollm3-3b-q4-k-m-gguf
  - Runtime: llamacpp
  - Engine: cpu
assumptions:
  - Host execution is CPU-only; ports 8356 and 8357 are reserved for hal9000-smollm3.
missing_inputs: none
blocking_issues: none
```
