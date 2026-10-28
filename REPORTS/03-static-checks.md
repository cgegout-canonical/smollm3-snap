# Stage 3: Inference Snap Static Checks Report

Workspace: `/home/cgegout/projects/smollm3`
Snap Name: `smollm3`

## Validation Results

### 1. Pre-flight & Schema Consistency
- `snap-name`: `hal9000-smollm3` matches regex `^[a-z0-9]+(-[a-z0-9]+)*$` (VALID).
- `models/smollm3-3b-q4-k-m-gguf/model.yaml`: `disk-size: 1827M` matches regex `^[0-9]+[KMG]$` (VALID).
- Model description adheres to SDK standards: no model parameter counts or file sizes in prose description.
- Engine/runtime/model naming agreements verified:
  - `engines/cpu/engine.yaml` references runtime `llamacpp` and model `smollm3-3b-q4-k-m-gguf` (EXISTS).
  - `runtimes/llamacpp/runtime.yaml` references component `llamacpp` (DECLARED in `snapcraft.yaml`).
  - `models/smollm3-3b-q4-k-m-gguf/model.yaml` references component `smollm3-3b-q4-k-m-gguf` (DECLARED in `snapcraft.yaml`).

### 2. Component Completeness
- `model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf` exists (1,915,306,528 bytes, sha256: `4de907d2d388a5508fb7cb443a06effe14cce3518b0a78d3bdd9e74d9edce989`).
- Declared components: `smollm3-3b-q4-k-m-gguf`, `llamacpp`.
- No empty or dangling component directories.

### 3. Engine Sanity & Executables
- `engines/cpu/server` is executable (`chmod +x`).
- `scripts/server.sh` and `scripts/server-webui.sh` are executable (`chmod +x`).
- `snap/hooks/install` and `snap/hooks/post-refresh` are executable (`chmod +x`).
- Hook fallback engine `--fallback=cpu` matches existing engine `cpu`.

### 4. Model Signature & Provenance
- Artifact: `SmolLM3-3B-Q4_K_M.gguf`
- Format: GGUF v3
- Metadata: `general.architecture = smollm3`, `general.name = Smollm3-3B`, `general.size_label = 3B`, `general.base_model.0.repo_url = https://huggingface.co/HuggingFaceTB/SmolLM3-3B`, `general.quantized_by = Unsloth`.
- Chat template: Unsloth SmolLM3 chat template with `<|im_start|>` and configurable reasoning modes (`/think`, `/no_think`).
- Verified SHA256: `4de907d2d388a5508fb7cb443a06effe14cce3518b0a78d3bdd9e74d9edce989`.

### 5. Host, Port, and Alias Consistency
- Port seeding in `install` hook: `http.port=8356`, `webui.http.port=8357`, `http.host=127.0.0.1`, `webui.http.host=127.0.0.1`.
- Verified ports 8356 and 8357 are free on loopback before packaging.
- CLI version pinned consistently across `snapcraft.yaml` and `.github/workflows/pr-checks.yaml` (`v2.0.0-beta.18`).

```pipeline-report
snapcraft_consistency: pass
component_completeness: pass
engine_sanity: pass
model_signature: pass
host_port_alias_consistency: pass

blocking_findings: []
non_blocking_findings: []

overall: pass
```
