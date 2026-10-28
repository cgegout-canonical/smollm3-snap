# SmolLM3 inference snap
[![smollm3](https://snapcraft.io/smollm3/badge.svg)](https://snapcraft.io/smollm3)

SmolLM3 is a compact large language model (LLM) developed by Hugging Face, designed for efficient natural language tasks such as text generation, summarization, reasoning, and question answering.

Use this snap to quickly install an optimized environment for local inference with SmolLM3.

The snap includes the following hardware-optimized inference engines:

* cpu: Optimized for x64 and ARM (armv8, armv9) CPUs
* nvidia-gpu: CUDA-enabled GPU acceleration

The most suitable engine is automatically selected based on the available hardware.

#### Install
```shell
sudo snap install smollm3
```

#### Run
```shell
smollm3
```

> [!TIP]
> Some accelerators require extra [drivers](https://documentation.ubuntu.com/inference-snaps/how-to/setup/drivers/) to be usable with this snap.

## Resources

📚 **[Documentation](https://documentation.ubuntu.com/inference-snaps/)**, learn how to use inference snaps

💬 **[Discussions](https://github.com/canonical/inference-snaps/discussions)**, ask questions and share ideas

🐛 **[Issues](https://github.com/canonical/inference-snaps/issues)**, report bugs and request features

## Build and install from source

Clone the repo:
```shell
git clone https://github.com/canonical/smollm3-snap
cd smollm3-snap
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
