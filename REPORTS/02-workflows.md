# Stage 2: GitHub Workflows Report

Snap Name: `hal9000-smollm3`
Repository: `canonical/hal9000-smollm3-snap`

## Adaptations & Configuration
1. **Repository & Snap References**:
   - Replaced `<snap-name>` with `hal9000-smollm3`.
   - Replaced `<inference-snap-repository>` with `hal9000-smollm3-snap`.
2. **CLI Alignment**:
   - Pinned `pr-checks.yaml` lint action to `canonical/inference-snaps-cli/.github/actions/lint-package@v2.0.0-beta.18`, aligning exactly with the `cli` part version in `snap/snapcraft.yaml`.
3. **Hardware & Capability Pruning**:
   - Text-only model: excluded all vision/image prompt flags (`test-image-prompt`).
   - CPU-only execution: excluded NVIDIA/Vulkan matrix entries from `pr-label.yaml`. Only the `cpu` engine test job is included (`maas-systemtests-amd64`).
   - Throughput baseline: excluded speculative/unverified `expected-tps` thresholds.
4. **Secret / Variable Requirements**:
   - Secrets: `STORE_LOGIN_MAIN`, `STORE_LOGIN_PR`, `OPENROUTER_API_KEY`, `ISSUE_CREATE_TOKEN`, `TESTFLINGER_SECRET_KEY`, `GITHUB_TOKEN`.
   - Variables: `TESTFLINGER_CLIENT_ID`.

```pipeline-report
{
  "stage": "github-workflows",
  "status": "pass",
  "workflow_files_created": [
    ".github/workflows/cicd.yaml",
    ".github/workflows/pr-checks.yaml",
    ".github/workflows/agentic-test.yaml",
    ".github/workflows/pr-label.yaml"
  ],
  "adaptations": [
    "Replaced snap name with hal9000-smollm3 and repository with canonical/hal9000-smollm3-snap",
    "Aligned lint action to v2.0.0-beta.18 matching snapcraft.yaml CLI part",
    "Pruned GPU test jobs from test matrix in pr-label.yaml; preserved single cpu engine job",
    "Pruned vision/image prompt capability flags"
  ],
  "required_secrets": ["STORE_LOGIN_PR", "STORE_LOGIN_MAIN", "OPENROUTER_API_KEY", "ISSUE_CREATE_TOKEN", "TESTFLINGER_SECRET_KEY"],
  "required_variables": ["TESTFLINGER_CLIENT_ID"],
  "issues": []
}
```
