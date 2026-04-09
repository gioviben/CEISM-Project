#!/bin/bash
#SBATCH --job-name=gradient_search_direction 
#SBATCH --nodes=1              # On descend à 2 nœuds pour respecter votre quota (QOS)
#SBATCH --ntasks=32            # OBLIGATOIRE : doit correspondre au Mesher (32)
#SBATCH --cpus-per-task=1      # On reste simple pour éviter de bloquer des ressources
#SBATCH --time=12:00:00
#SBATCH --output=output.%j
#SBATCH --error=error.%j
#SBATCH --partition=cpu_prod
#SBATCH --qos=16nodespu

set -euo pipefail

module purge
module load sem3d/2024.02.22/intel-2021.9.0-intel-oneapi-mpi

CONFIG_FILE="./gradient_search_parameters_file.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Missing config file: $CONFIG_FILE"
    exit 1
fi

eval "$(
CONFIG_FILE="$CONFIG_FILE" python - <<'PY'
import json
import os
import shlex

config_file = os.environ["CONFIG_FILE"]

with open(config_file, "r", encoding="utf-8") as f:
    cfg = json.load(f)

print(f"ITER={shlex.quote(str(cfg['iteration']))}")
print(f"LBFGS_MEM={shlex.quote(str(cfg['lbfgs_mem']))}")
print(f"STATE_DIR={shlex.quote(str(cfg['state_dir']))}")
print(f"OUTPUT_DIR={shlex.quote(str(cfg['output_dir']))}")
print(f"PYTHON_SCRIPT={shlex.quote(str(cfg['python_script']))}")
print(f"MPI_RANKS={shlex.quote(str(cfg['mpi_ranks']))}")
PY
)"

echo "ITER=$ITER"
echo "LBFGS_MEM=$LBFGS_MEM"
echo "STATE_DIR=$STATE_DIR"
echo "OUTPUT_DIR=$OUTPUT_DIR"
echo "PYTHON_SCRIPT=$PYTHON_SCRIPT"
echo "MPI_RANKS=$MPI_RANKS"


mpirun -n "$MPI_RANKS" python "$PYTHON_SCRIPT" \
    --iter "$ITER" \
    --lbfgs-mem "$LBFGS_MEM" \
    --state-dir "$STATE_DIR" \
    --output-dir "$OUTPUT_DIR"