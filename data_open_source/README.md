# Data Open Source Repository

Since the Artifact Evaluation phase of the paper requires reviewing the data behind the paper's figures and tables, the relevant data has been updated here.

This repository contains the plotting scripts (Python) corresponding to each figure in the paper, along with the raw log data they reference. All log paths in the scripts have been changed to relative paths, so you can reproduce the paper's figures simply by running them in this directory.

## Mapping between Code and Paper Figures

| Script File | Corresponding Paper Figure |
| --- | --- |
| `plot_simai_clem_nccl_pattern.py` | Figure 2 |
| `plot_bus_bw_intra_2x2.py` | Figure 8 |
| `plot_bus_bw_multi_2x2.py` | Figure 9 |
| `plot_msccl_simai_clem_truth_2x2.py` | Figure 10 |
| `plot_qplb_c4p_baseline_simai_clem_truth_1to1_v2.py` | Figure 11 |

## Data File Descriptions

- `astra_sim_256M.log`: ASTRA-sim 256MB AllReduce simulation log (referenced by `plot_simai_clem_nccl_pattern.py`)
- `SimAI_allreduce_256M.log`: SimAI 256MB AllReduce simulation log (referenced by `plot_simai_clem_nccl_pattern.py`)
- `d0908_test_profiling_256M_with_1qp_split.log`: NCCL-tests 256MB AllReduce measured log (referenced by `plot_simai_clem_nccl_pattern.py`)
- The experimental data for the remaining scripts (Figures 8/9/10/11) is embedded directly in their respective Python code

## How to Run

Dependencies: Python 3, matplotlib, numpy

```bash
python3 plot_simai_clem_nccl_pattern.py
python3 plot_bus_bw_intra_2x2.py
python3 plot_bus_bw_multi_2x2.py
python3 plot_msccl_simai_clem_truth_2x2.py
python3 plot_qplb_c4p_baseline_simai_clem_truth_1to1_v2.py
```

The PDF/PNG figure files generated after running will be output to the current directory.
