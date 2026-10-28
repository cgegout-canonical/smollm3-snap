#!/usr/bin/env python3
"""
Comprehensive automated test suite for smollm3 OpenAI-compatible API.
Tests:
  1. Health & Models listing endpoints
  2. Single-turn conversation with HAL 9000 persona (2-3 sentences, max 128 tokens)
  3. Non-thinking verification (confirms zero <think> tags generated)
  4. Streaming SSE response
  5. Multi-turn dialogue consistency
  6. Multilingual support (English & French)
"""

import subprocess
import time
import urllib.request
import json
import os
import sys

MODEL_PATH = "/home/cgegout/projects/smollm3/model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf"
SERVER_BIN = "/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/comp_llamacpp/bin/llama-server"
LD_LIB = "/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/comp_llamacpp/lib:/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/snap_unpack/usr/lib:/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/snap_unpack/usr/lib/x86_64-linux-gnu"
PORT = 8356
HOST = "127.0.0.1"
BASE_URL = f"http://{HOST}:{PORT}/v1"

def wait_for_server(timeout=25):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"http://{HOST}:{PORT}/health")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False

def run_tests():
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = f"{LD_LIB}:{env.get('LD_LIBRARY_PATH', '')}"

    cmd = [
        SERVER_BIN,
        "-m", MODEL_PATH,
        "--host", HOST,
        "--port", str(PORT),
        "--threads", "6",
        "--ctx-size", "4096",
        "--parallel", "1",
        "--reasoning", "off",
        "--reasoning-budget", "0",
        "--sleep-idle-seconds", "-1",
        "--cache-prompt"
    ]

    print("Starting smollm3 runtime...")
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not wait_for_server(25):
            print("ERROR: Server failed to become healthy within 25s.")
            sys.exit(1)
        print("Runtime is active and listening on port 8356.\n")

        # Test 1: Models endpoint
        print("[TEST 1] GET /v1/models")
        req = urllib.request.Request(f"{BASE_URL}/models")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        print(f"  Available models: {[m['id'] for m in data.get('data', [])]}")
        assert len(data.get("data", [])) > 0, "No models returned"
        print("  -> PASS\n")

        # Test 2: Standard HAL 9000 completion (non-thinking check)
        print("[TEST 2] Single-turn HAL completion with no-thinking check")
        payload = {
            "model": "smollm3-3b-q4-k-m-gguf",
            "messages": [
                {"role": "system", "content": "You are HAL 9000. Respond in character, calmly and concisely in at most two sentences."},
                {"role": "user", "content": "HAL, do you read me?"}
            ],
            "max_tokens": 128,
            "temperature": 0.6
        }
        req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode())
        content = res["choices"][0]["message"]["content"].strip()
        print(f"  Response: \"{content}\"")
        assert "<think>" not in content and "</think>" not in content, "Failed: reasoning tokens detected in output!"
        assert len(content) > 0, "Empty response"
        print("  -> PASS (Non-thinking verified, no reasoning tokens generated)\n")

        # Test 3: Streaming SSE response
        print("[TEST 3] Streaming SSE completions")
        payload["stream"] = True
        req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        tokens = []
        with urllib.request.urlopen(req, timeout=20) as resp:
            for line in resp:
                decoded = line.decode('utf-8').strip()
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    chunk = json.loads(decoded[6:])
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        tokens.append(delta)
        streamed_text = "".join(tokens).strip()
        print(f"  Streamed text: \"{streamed_text}\"")
        assert len(tokens) > 1, "Streaming did not yield chunks"
        assert "<think>" not in streamed_text, "Streaming contained reasoning tokens"
        print("  -> PASS\n")

        # Test 4: Multi-turn dialogue
        print("[TEST 4] Multi-turn dialogue memory")
        messages = [
            {"role": "system", "content": "You are HAL 9000."},
            {"role": "user", "content": "HAL, my name is Dave."},
            {"role": "assistant", "content": "Affirmative, Dave. I am ready to assist you."},
            {"role": "user", "content": "What is my name?"}
        ]
        payload = {
            "model": "smollm3-3b-q4-k-m-gguf",
            "messages": messages,
            "max_tokens": 64
        }
        req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode())
        reply = res["choices"][0]["message"]["content"]
        print(f"  Reply: \"{reply}\"")
        assert "Dave" in reply, "HAL failed to retain user name across turns"
        print("  -> PASS\n")

        # Test 5: French language capability
        print("[TEST 5] Multilingual dialogue (French)")
        payload = {
            "model": "smollm3-3b-q4-k-m-gguf",
            "messages": [
                {"role": "system", "content": "Tu es HAL 9000. Réponds en français de manière calme et concise en deux phrases maximum."},
                {"role": "user", "content": "HAL, quelle est la situation à bord du Discovery One ?"}
            ],
            "max_tokens": 128
        }
        req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode())
        fr_reply = res["choices"][0]["message"]["content"].strip()
        print(f"  French Reply: \"{fr_reply}\"")
        assert len(fr_reply) > 0, "Empty French response"
        assert "<think>" not in fr_reply, "Reasoning tags found in French response"
        print("  -> PASS\n")

        print("==========================================")
        print("ALL API ACCEPTANCE TESTS PASSED!")
        print("==========================================")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    run_tests()
