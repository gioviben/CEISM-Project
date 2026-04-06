#!/bin/bash
#SBATCH --job-name=SOLVER 
#SBATCH --nodes=16
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=2
#SBATCH --time=12:00:00
#SBATCH --output=ro.txt 
#SBATCH --error=re.txt 
#SBATCH --partition=cpu_prod
#SBATCH --qos=16nodespu

module load sem3d/2024.02.22/intel-2021.9.0-intel-oneapi-mpi

ulimit -s unlimited
mpirun -n $SLURM_NTASKS sem3d.exe > output.solver
