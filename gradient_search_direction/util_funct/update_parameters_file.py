import json
from pathlib import Path

def update_parameters_file(parameters_file_path, n_iter, LBFGS_MEM, LBFGS_STATE_FOLDER_PATH, LBFGS_OUTPUT_FOLDER_PATH):
    
    job_cfg = {
        "iteration": n_iter,
        "lbfgs_mem": LBFGS_MEM,
        "state_dir": str(LBFGS_STATE_FOLDER_PATH),
        "output_dir": str(LBFGS_OUTPUT_FOLDER_PATH),
        "mpi_ranks": 32,
        "python_script": "compute_gradient_search_direction.py",
    }

    with open(parameters_file_path, "w", encoding="utf-8") as f:
        json.dump(job_cfg, f, indent=2)