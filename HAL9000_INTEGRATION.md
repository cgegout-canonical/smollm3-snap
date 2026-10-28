# HAL9000 Client Integration Guide

This document describes how to configure HAL9000 to interact with the local `smollm3` inference service.

## 1. Service Endpoints
- **Base URL**: `http://127.0.0.1:8356/v1`
- **Chat Completions**: `http://127.0.0.1:8356/v1/chat/completions`
- **Models Endpoint**: `http://127.0.0.1:8356/v1/models`
- **Health Check**: `http://127.0.0.1:8356/health`
- **Web UI**: `http://127.0.0.1:8357`

## 2. Model Configuration
- **Model Identifier**: `smollm3-3b-q4-k-m-gguf`
- **Context Size**: `4096` tokens
- **Inference Slots**: `1` (dedicated single-client low latency)
- **Idle Timeout**: Disabled (`--sleep-idle-seconds -1`), model stays resident in RAM.
- **Prompt Caching**: Enabled (`--cache-prompt`).
- **Reasoning / Extended Thinking**: Disabled (`--reasoning off`, `--reasoning-budget 0`).

## 3. Recommended Client Persona & System Prompt
To maintain HAL 9000's voice and guarantee low-latency conversational responses:

```text
You are HAL 9000, the shipboard artificial intelligence on Discovery One.
Respond calmly, rationally, and concisely in at most two or three sentences.
Do not output internal monologue or thinking tokens.
```

## 4. Integration Examples

### A. cURL Example
```bash
curl -X POST http://127.0.0.1:8356/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm3-3b-q4-k-m-gguf",
    "messages": [
      {
        "role": "system",
        "content": "You are HAL 9000. Respond calmly and concisely in two sentences."
      },
      {
        "role": "user",
        "content": "HAL, what is the status of the AE-35 communication unit?"
      }
    ],
    "max_tokens": 128,
    "temperature": 0.6
  }'
```

### B. Python (OpenAI SDK) Example
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8356/v1",
    api_key="unused"
)

response = client.chat.completions.create(
    model="smollm3-3b-q4-k-m-gguf",
    messages=[
        {
            "role": "system",
            "content": "You are HAL 9000. Respond calmly and concisely in at most two sentences."
        },
        {
            "role": "user",
            "content": "Open the pod bay doors, HAL."
        }
    ],
    max_tokens=128,
    temperature=0.6,
    stream=False
)

print(response.choices[0].message.content)
```

### C. Streaming SSE Client (Python)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8356/v1",
    api_key="unused"
)

stream = client.chat.completions.create(
    model="smollm3-3b-q4-k-m-gguf",
    messages=[
        {"role": "system", "content": "You are HAL 9000. Keep answers under 3 sentences."},
        {"role": "user", "content": "Give me a diagnostic report on engine telemetry."}
    ],
    max_tokens=128,
    stream=True
)

for chunk in stream:
    token = chunk.choices[0].delta.content or ""
    print(token, end="", flush=True)
print()
```
