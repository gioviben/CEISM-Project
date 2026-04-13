# ST7 – Virtual Seismic Imaging with SEM3D

HPC project for **3D seismic imaging** using **SEM3D**, the **adjoint-state method**, and a **Full-Waveform Inversion (FWI)** workflow to estimate subsurface **Lamé parameters** (`λ`, `μ`).

## Overview

The workflow includes:
- forward simulation with **SEM3D**
- misfit computation between simulated and observed traces
- adjoint simulation with time-reversed residuals
- gradient and search direction computation (L-BFGS)
- material update

## Repository structure

```text
.
├── gradient_search_direction/  # gradient + L-BFGS search direction
├── match/                      # material models used for a test
├── materials_samples/          # material models
├── pysem/                      # SEM3D Python utilities
├── sem3d_config_files/         # forward simulation configs
├── sem3d_config_files_adj/     # adjoint simulation configs
├── util_funct/                 # helper functions
├── main.ipynb                  # main inversion workflow
├── pyproject.toml              # project config
└── README.md
