#!/usr/bin/env bash
set -euo pipefail

MODEL_SOURCE_DIR="${MODEL_SOURCE_DIR:-/home/cgegout/projects/smollm3_old}"
TARGET_DIR="model-weights/smollm3-3b-q4-k-m-gguf"
TARGET_FILE="${TARGET_DIR}/SmolLM3-3B-Q4_K_M.gguf"
SOURCE_FILE="${MODEL_SOURCE_DIR}/model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf"

mkdir -p "${TARGET_DIR}"

if [[ -f "${SOURCE_FILE}" ]]; then
    echo "Reflinking/copying local model weights from ${SOURCE_FILE}..."
    cp --reflink=auto "${SOURCE_FILE}" "${TARGET_FILE}"
else
    echo "Local source model not found at ${SOURCE_FILE}" >&2
    exit 1
fi

echo "Model weights prepared at ${TARGET_FILE}"
ls -lh "${TARGET_FILE}"
