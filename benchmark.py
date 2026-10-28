#!/usr/bin/env python3
"""
Repeatable benchmark script for hal9000-smollm3 CPU inference.
Compares 4 threads, 6 threads (6 P-cores), and 8 threads.
Measures:
  - Startup latency
  - First-token latency (TTFT)
  - Total latency
  - Generation speed (tokens/sec)
  - Resident memory (RSS)
"""

import subprocess
import time
import urllib.request
import json
import os
import signal
import sys

MODEL_PATH = "/home/cgegout/projects/hal9000-smollm3-snap/model-weights/smollm3-3b-q4-k-m-gguf/SmolLM3-3B-Q4_K_M.gguf"
SERVER_BIN = "/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/comp_llamacpp/bin/llama-server"
LD_LIB = "/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/comp_llamacpp/lib:/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/snap_unpack/usr/lib:/home/cgegout/projects/hal9000-smollm3-snap/build-scratch/snap_unpack/usr/lib/x86_64-linux-gnu"
PORT = 8356
HOST = "127.0.0.1"
API_URL = f"http://{HOST}:{PORT}/v1/chat/completions"
HEALTH_URL = f"http://{HOST}:{PORT}/health"

TEST_PROMPTS = [
    "HAL, summarize the status of the communication antenna in two short sentences.",
    "HAL, what is the mission objective for Jupiter orbit insertion?",
    "Explain quantum entanglement simply in two sentences.",
    "State three essential safety protocols for EVA operations in two sentences.",
    "HAL, calculate remaining life support reserves and reply in two concise sentences.",
    "Describe the primary propulsion mechanism of Discovery One in two sentences.",
    "HAL, are all ship systems nominal? Reply briefly.",
    "What is the difference between supervised and unsupervised learning in two sentences?",
    "HAL, what should we do if AE-35 unit fails? Answer in two sentences.",
    "Summarize your primary directive as ship AI in two concise sentences."
]

def wait_for_server(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(HEALTH_URL)
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    return time.time() - start
        except Exception:
            time.sleep(0.3)
    return None

def get_process_rss_mb(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    parts = line.split()
                    return int(parts[1]) / 1024.0 # MB
    except Exception:
        pass
    return 0.0

def run_benchmark(threads):
    print(f"\n==========================================")
    print(f"Benchmarking with {threads} threads")
    print(f"==========================================")
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = f"{LD_LIB}:{env.get('LD_LIBRARY_PATH', '')}"

    cmd = [
        SERVER_BIN,
        "-m", MODEL_PATH,
        "--host", HOST,
        "--port", str(PORT),
        "--threads", str(threads),
        "--ctx-size", "4096",
        "--parallel", "1",
        "--reasoning", "off",
        "--reasoning-budget", "0",
        "--sleep-idle-seconds", "-1",
        "--cache-prompt"
    ]

    t0 = time.time()
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        startup_time = wait_for_server(30)
        if startup_time is None:
            print("Failed to start server within 30s")
            return None
        print(f"Server ready in {startup_time:.2f}s")

        # Warmup request
        warmup_payload = json.dumps({
            "model": "smollm3-3b-q4-k-m-gguf",
            "messages": [{"role": "user", "content": "Hello HAL"}],
            "max_tokens": 16
        }).encode("utf-8")
        req = urllib.request.Request(API_URL, data=warmup_payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()

        latencies = []
        tokens_list = []
        tok_per_sec_list = []

        for i, prompt in enumerate(TEST_PROMPTS):
            payload = json.dumps({
                "model": "smollm3-3b-q4-k-m-gguf",
                "messages": [
                    {"role": "system", "content": "You are HAL 9000. Respond calmly, concisely, in at most two or three sentences."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 128,
                "temperature": 0.6
            }).encode("utf-8")

            t_req_start = time.time()
            req = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t_req_start

            completion_tokens = body.get("usage", {}).get("completion_tokens", 0)
            tps = completion_tokens / elapsed if elapsed > 0 else 0

            latencies.append(elapsed)
            tokens_list.append(completion_tokens)
            tok_per_sec_list.append(tps)

            content = body["choices"][0]["message"]["content"]
            # verify no reasoning tags
            has_think = "<think>" in content or "</think>" in content
            print(f"  Req {i+1:02d}: {elapsed:.2f}s | {completion_tokens} tok | {tps:.1f} t/s | Think tags: {'YES (FAIL)' if has_think else 'NO (PASS)'}")

        rss_mb = get_process_rss_mb(proc.pid)
        avg_latency = sum(latencies) / len(latencies)
        avg_tps = sum(tok_per_sec_list) / len(tok_per_sec_list)

        return {
            "threads": threads,
            "startup_sec": startup_time,
            "avg_latency_sec": avg_latency,
            "min_latency_sec": min(latencies),
            "max_latency_sec": max(latencies),
            "avg_tok_per_sec": avg_tps,
            "rss_mb": rss_mb
        }

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        time.sleep(1)

if __name__ == "__main__":
    configs = [4, 6, 8]
    summary = []
    for c in configs:
        res = run_benchmark(c)
        if res:
            summary.append(res)

    print("\n================ BENCHMARK SUMMARY ================")
    print(f"{'Threads':<10}{'Startup (s)':<15}{'Avg Latency (s)':<18}{'Avg Tok/s':<15}{'RSS (MB)':<12}")
    for s in summary:
        print(f"{s['threads']:<10}{s['startup_sec']:<15.2f}{s['avg_latency_sec']:<18.2f}{s['avg_tok_per_sec']:<15.1f}{s['rss_mb']:<12.1f}")
