# SimAI-CLEM: Collective communication Library EMulator
## SimAI-CLEM Introduction
SimAI-CLEM (Collective communication Library EMulator) is a novel Collective Communications Library (CCL) emulator that achieves three key goals: easy-to-deploy, high fidelity and high scalability. To this end, SimAI-CLEM runs the vanilla CCL directly on the GPU hardware, while intercepting its P2P communication primitives and redirecting them to a mature network simulator. In addition, SimAI-CLEM incorporates several optimization techniques to enable a 96x increase in emulation scale on a single GPU.

We have implemented the network simulator of SimAI-CLEM based on the ns-3 component of SimAI, and adapt it to [NCCL](https://github.com/NVIDIA/nccl) v2.23.4 and [MSCCLExecutor](https://github.com/Azure/msccl-executor-nccl) v2.23.4. Experimental results show that SimAI-CLEM is capable of accurately modeling CCL's performance under non-stationary network conditions and after the deployment of optimization strategies. SimAI-CLEM offers valuable insights for optimizing CCLs, thereby enhancing the efficiency of end-to-end LLM training and inference.

## Open-Source Roadmap

We are open-sourcing SimAI-CLEM in a step-by-step manner. The plan and the current status are summarized below:

| Item | Status |
| :--- | :----- |
| SimAI-CLEM adaptation for [NCCL](https://github.com/NVIDIA/nccl) | ✅ Completed |
| SimAI-CLEM adaptation for [MSCCLExecutor](https://github.com/Azure/msccl-executor-nccl) | 🚧 In Progress |
| ns-3 ↔ CCL IPC via shared memory | ✅ Completed |
| ns-3 ↔ CCL IPC via TCP socket | 🚧 In Progress |

## Architecture Overview

SimAI-CLEM operates through a modular architecture composed of three primary components:

### 1. `simulator-network`

> **Repository Notice**: The `simulator-network` component is in [`aliyun/ns-3-alibabacloud`](https://github.com/aliyun/ns-3-alibabacloud) — and is maintained on the [`feat/ipc-middleware`](https://github.com/aliyun/ns-3-alibabacloud/tree/feat/ipc-middleware) branch. Please clone that repository and check out this branch to obtain the network simulator component described below.

This section contains the key components of SimAI-CLEM as follows:
- **Actual Data Transfer Engine**: Handles essential control-message exchanges between CCL processes. 
- **Network Simulator Middleware**: Mediates interactions between application-level communication requests and the network simulator (e.g., [ns-3](https://www.nsnam.org/)).
- **ns-3 Backend**: Leverages the ns-3 component of SimAI as the underlying network emulator.

We extend ns-3 with custom classes to support IBV Verbs-like interfaces:
- `IbvQP`: Models Queue Pairs for reliable and connection-oriented communication.
- `IbvCQ`: Implements Completion Queues for asynchronous operation notification.
- `IbvInterface` / `IbvInterfaceHelper`: Provide abstraction layers for virtualized NIC functionality.

These components collectively allow ns-3 to parse, execute, and respond to IBV-style communication calls issued by upper-layer applications such as NCCL. For detailed design rationale and class relationships, please refer to documentation under `./docs/` and inline code comments.

### 2. `nccl_hack_rdma`

> **Distribution**: provided as [`nccl_patch`](./nccl_patch), applied on top of upstream [NCCL](https://github.com/NVIDIA/nccl) at commit `2ea4ee94bfb04c886c79ccae60ac9961000fdee2`. See the [Quick Start Guide](#quick-start-guide).

Based on NVIDIA's open-source [NCCL](https://github.com/NVIDIA/nccl) library (commit ID: 2ea4ee94bfb04c886c79ccae60ac9961000fdee2), this component introduces several key enhancements:
- **API Navigator**: A new subsystem located in `src/nsibverbs/`, responsible for capturing and rerouting RDMA-related system calls (e.g., `ibv_post_send`) to the simulation middleware.
- **Configurable Hardware Adapter**: Enables flexible configuration of hardware characteristics (e.g., bandwidth, latency) without modifying application logic.
- **Optimizations for Large-Scale Emulation**: Includes  hostname hijacking, the memory reuse mechanism and the multi-machine emulation method that improve simulation scalability.

The modifications preserve functional correctness while decoupling communication semantics from physical transport dependencies.

### 3. `nccl-tests-modify`

> **Distribution**: provided as [`nccl_tests_patch`](./nccl_tests_patch), applied on top of upstream [`nccl-tests`](https://github.com/NVIDIA/nccl-tests) at commit `8dfeab9eb9bdfdf13503e71e1f33e7f8a208b540`. See the [Quick Start Guide](#quick-start-guide).

An extended version of [`nccl-tests`](https://github.com/NVIDIA/nccl-tests) (commit ID: 8dfeab9eb9bdfdf13503e71e1f33e7f8a208b540) that provides:
- An additional interface allowing direct access to **simulation time** within ns-3 via an Inter-Process Communication (IPC) mechanism.
- Further optimizations aligned with large-scale emulation requirements, such as hostname hijacking and the memory reuse mechanism.

This enables precise correlation between application progress and simulated network dynamics.

## Quick Start Guide

> **Distribution note**: This repository ships SimAI-CLEM's changes to NCCL and nccl-tests as two patches — [`nccl_patch`](./nccl_patch) and [`nccl_tests_patch`](./nccl_tests_patch) — rather than full source trees. Apply each patch on top of the exact upstream commit specified below to reconstruct the SimAI-CLEM-modified sources.

### Step 1: Reconstruct the Modified NCCL (`nccl_hack_rdma`)

```bash
git clone https://github.com/NVIDIA/nccl.git nccl_hack_rdma
cd nccl_hack_rdma
# nccl_patch targets this exact upstream commit (NCCL v2.23.4 series):
git checkout 2ea4ee94bfb04c886c79ccae60ac9961000fdee2
git apply /path/to/SimAI-CLEM/nccl_patch
```

### Step 2: Compile the Modified NCCL

```bash
# still inside the nccl_hack_rdma directory
make clean
make -j src.build
```

After compilation, the built artifacts will be available under `nccl_hack_rdma/build/`.

> Note: Record the absolute path to this directory; it will be required in subsequent steps.

### Step 3: Build the ns-3 Binary

```bash
# NOTE: `simulator-network` is NOT in this repository.
# First clone https://github.com/aliyun/ns-3-alibabacloud and check out its feat/ipc-middleware branch,
# then switch to that branch's directory before running the commands below.
cd simulator-network/simulation/
source build.sh # see build.sh for more details
```

### Step 4: Reconstruct & Compile the Instrumented NCCL Tests (`nccl-tests-modify`)

```bash
git clone https://github.com/NVIDIA/nccl-tests.git nccl-tests-modify
cd nccl-tests-modify
# nccl_tests_patch targets this exact upstream commit (nccl-tests v2.13.11):
git checkout 8dfeab9eb9bdfdf13503e71e1f33e7f8a208b540
git apply /path/to/SimAI-CLEM/nccl_tests_patch
```

Replace `{MPI_ABS_PATH}` and `{NCCL_HACK_RDMA_ABS_PATH}` with the actual absolute paths, then compile:

```bash
make MPI=1 MPI_HOME={MPI_ABS_PATH} NCCL_HOME={NCCL_HACK_RDMA_ABS_PATH}/build
```

### Step 5: Run the Emulation

#### Phase A: Launch the ns-3 Backend

Start the ns-3 simulation engine first. Use the following command:

```bash
# NOTE: `simulator-network` is NOT in this repository.
# First clone https://github.com/aliyun/ns-3-alibabacloud and check out its feat/ipc-middleware branch,
# then switch to that branch's directory before running the commands below.
cd simulator-network/simulation/
./ns3 run 'scratch/QpReuseSimInfra {CONFIG_FILE_PATH} --numnodes={NUM_RANKS}'
# For example:
# ./ns3 run 'scratch/QpReuseSimInfra mix/incast/config_example.sh --numnodes=16'
```

- `{CONFIG_FILE_PATH}`: Absolute path to a valid configuration script
- `{NUM_RANKS}`: Number of ranks in the collective communication task

Example configuration files can be found at:
```
# NOTE: located in the feat/ipc-middleware branch of aliyun/ns-3-alibabacloud (not in this repository)
simulator-network/simulation/mix/incast/config_example.sh
```
which includes comprehensive documentation of tunable parameters such as topology, NIC settings, etc.

#### Phase B: Launch the NCCL Application

Ensure the ns-3 backend is running before starting the nccl-tests processes.

```bash
# See run_nccl_16A100.sh for more details.  
source run_nccl_16A100.sh
```


> **Tested Platform**: So far, we have only conducted experiments on servers equipped with **8x A100 GPUs**. The code in this project has not yet been tested on any other platform.

> **GPU-Free Demo**: To let users learn and understand the design philosophy of SimAI-CLEM's **bidirectional interaction framework** even without access to a GPU environment, we provide a demo example under [`RDMA_demo`](https://github.com/aliyun/ns-3-alibabacloud/tree/feat/ipc-middleware/RDMA_demo) in the `simulator-network` repository.

> ⚠️ Important: The order of execution matters. The ns-3 simulation must be started prior to launching any NCCL rank to ensure proper IPC handshake and initialization.

## Documentation and Extensibility

For architectural diagrams, API specifications, and guidance on extending SimAI-CLEM for custom use cases (e.g., supporting new NCCL collectives or alternative simulators), please consult the documentation suite in `./docs/`.

## Citation

If you use SimAI-CLEM in academic research, please consider citing our associated publication (to be updated upon release).

## License

This repository (SimAI-CLEM) as a whole, including all modifications made by the SimAI-CLEM authors, is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). See [`LICENSE`](./LICENSE) for the full text and [`NOTICE`](./NOTICE) for attribution details.

SimAI-CLEM is a derivative work of third-party open-source components. This repository distributes those derivatives as **patches** ([`nccl_patch`](./nccl_patch), [`nccl_tests_patch`](./nccl_tests_patch)) that you apply on top of the upstream projects; the upstream copyright and license notices are preserved in the reconstructed source trees and are also recorded in [`NOTICE`](./NOTICE):

- [`nccl_patch`](./nccl_patch) modifies NVIDIA's [NCCL](https://github.com/NVIDIA/nccl) (v2.23.4, commit `2ea4ee94bfb04c886c79ccae60ac9961000fdee2`), originally released under the **BSD 3-Clause License** (its `LICENSE.txt` ships with the upstream tree). The patched tree also bundles headers from the [NVIDIA Tools Extension SDK (NVTX)](https://github.com/NVIDIA/NVTX), licensed under **Apache-2.0 WITH LLVM-exception**.
- [`nccl_tests_patch`](./nccl_tests_patch) modifies NVIDIA's [nccl-tests](https://github.com/NVIDIA/nccl-tests) (v2.13.11), originally released under the **BSD 3-Clause License** (its `LICENSE.txt` ships with the upstream tree).
