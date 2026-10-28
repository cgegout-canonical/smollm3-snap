---
snap-name: hal9000-smollm3
snap-title: HAL9000 SmolLM3
model-card: https://huggingface.co/unsloth/SmolLM3-3B-GGUF
http-port: 8356
webui-http-port: 8357
engines: cpu
---

# HAL9000 SmolLM3 inference snap
[![hal9000-smollm3](https://snapcraft.io/hal9000-smollm3/badge.svg)](https://snapcraft.io/hal9000-smollm3)

SmolLM3 is a compact large language model optimized for low-latency conversations, reasoning, and instruction-following tasks.

Use this snap to quickly install an optimized environment for local inference with HAL9000 SmolLM3.

The snap includes the following hardware-optimized inference engines:

* cpu: Optimized for x64 CPUs with AVX2 and AVX-VNNI support

The CPU engine is automatically selected for host execution without requiring GPU drivers.

#### Install
```shell
sudo snap install hal9000-smollm3
```

#### Run
```shell
hal9000-smollm3
```

## Resources

📚 **[Documentation](https://documentation.ubuntu.com/inference-snaps/)**, learn how to use inference snaps

💬 **[Discussions](https://github.com/canonical/inference-snaps/discussions)**, ask questions and share ideas

🐛 **[Issues](https://github.com/canonical/inference-snaps/issues)**, report bugs and request features

## Build and install from source

Clone the repo:
```shell
git clone https://github.com/canonical/hal9000-smollm3-snap
cd hal9000-smollm3-snap
```

Initialize the development environment:
```shell
make init
```

Build and install snap:
```shell
make build
make install
```
