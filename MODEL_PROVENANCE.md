# Model Provenance: SmolLM3-3B Q4_K_M GGUF

## 1. Artifact Identity
- **Model Name**: SmolLM3-3B (Instruction-Tuned)
- **Architecture**: `smollm3` (Llama-style architecture, 3 Billion parameters)
- **File Name**: `SmolLM3-3B-Q4_K_M.gguf`
- **File Size**: `1,915,306,528 bytes` (~1.82 GB)
- **Local SHA256**: `4de907d2d388a5508fb7cb443a06effe14cce3518b0a78d3bdd9e74d9edce989`
- **Quantization Type**: `Q4_K_M` (4-bit medium k-quantization)
- **Format**: GGUF v3 (`little endian`)

## 2. Upstream Provenance & Attribution
- **Originating Repository**: [HuggingFaceTB/SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B)
- **Developer**: Hugging Face Team (SmolLM Project)
- **Quantizer / Source Package**: Quantized via Unsloth tooling from official FP16/BF16 instruction-tuned checkpoint (`SmolLM3-3B-Instruct`).
- **Base Model URL**: `https://huggingface.co/HuggingFaceTB/SmolLM3-3B`
- **License**: Apache 2.0 (Commercial and private use permitted)

## 3. Extracted GGUF Metadata
Inspection of the header via llama.cpp metadata parser confirmed:
- `general.architecture`: `smollm3`
- `general.name`: `Smollm3-3B`
- `general.size_label`: `3B`
- `general.type`: `model`
- `general.version`: `v3`
- `general.quantization_version`: `2`
- `llama.context_length`: `8192` (configured to `4096` in this snap for laptop memory/cache optimization)
- `llama.embedding_length`: `2048`
- `llama.block_count`: `36`
- `llama.feed_forward_length`: `8192`
- `llama.attention.head_count`: `16`
- `llama.attention.head_count_kv`: `4` (Grouped Query Attention)
- `llama.rope.freq_base`: `1000000.0`
- `tokenizer.ggml.model`: `gpt2` / `llama` BPE
- `tokenizer.chat_template`: `<|im_start|>` ChatML format with thinking block support (`/think`, `/no_think`)

## 4. Local Ingestion & Reproducibility
- **Source Directory**: Discovered in `/home/cgegout/projects/smollm3_old/model-weights/smollm3-3b-q4-k-m-gguf/`
- **Integrity Verification**: SHA256 checksum matched byte-for-byte.
- **Copy Mechanism**: Copied via `cp --reflink=auto` (preserving disk space on copy-on-write filesystems) into `model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf`.
- **Repeatable Preparation**: Encapsulated in `prepare_model.sh` with environment variable `MODEL_SOURCE_DIR` defaulting to `/home/cgegout/projects/smollm3_old`.
