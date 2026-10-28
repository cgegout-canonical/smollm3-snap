SHELL := /bin/bash

# Always run `hf` via pipx to avoid relying on local `hf` installations.
hf := pipx run --spec "huggingface_hub[cli]" hf

SNAP_NAME ?= hal9000-smollm3
ENGINE ?= cpu
MODEL_SOURCE_DIR ?= /home/cgegout/projects/smollm3_old

.PHONY: all help init build install upload smoke-test install-deps init-submodules download-models download-model-3b

all: help

#
# Main targets
#

help: ## Show this help message
	@echo "Usage: make <target>"
	@echo
	@echo "Targets:"
	@# List all targets with descriptions (lines starting with '##'):
	@grep -E '^[a-zA-Z0-9_-]+:.*## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  %-11s %s\n", $$1, $$2}'

init: init-submodules install-deps download-models ## Initialize the build environment (dependencies, model weights, submodules, etc.)

build: ## Build the snap
	./dev/build.sh

install: ## Install the snap
	./dev/install.sh

upload: ## Upload the snap
	./dev/upload.sh

smoke-test: ## Run smoke tests (override with SNAP_NAME=... ENGINE=...)
	sudo ./dev/smoke-test.sh $(SNAP_NAME) $(ENGINE)

#
# Supporting targets
#

install-deps:
	@echo "Installing dependencies..."
	@command -v pipx >/dev/null 2>&1 || { \
		echo "pipx missing; install via apt if privileges allow."; \
	}

init-submodules:
	@echo "Initializing submodules..."
	@if git submodule status | grep -q '^-'; then \
		git submodule update --init; \
	fi

download-models: download-model-3b

download-model-3b:
	@echo "Preparing SmolLM3-3B Q4_K_M model weights..."
	@mkdir -p model-weights/smollm3-3b-q4-k-m-gguf
	@if [ -f "$(MODEL_SOURCE_DIR)/model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf" ]; then \
		echo "Reflinking/copying local model weights from $(MODEL_SOURCE_DIR)..."; \
		cp --reflink=auto "$(MODEL_SOURCE_DIR)/model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf" \
			model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf; \
	else \
		echo "Local model not found at $(MODEL_SOURCE_DIR). Downloading via huggingface CLI..."; \
		$(hf) download unsloth/SmolLM3-3B-GGUF \
			SmolLM3-3B-Q4_K_M.gguf \
			--local-dir model-weights/smollm3-3b-q4-k-m-gguf/; \
	fi
