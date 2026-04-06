#!/bin/bash
#SBATCH --job-name=SOLVER 
#SBATCH --nodes=1              # On descend à 2 nœuds pour respecter votre quota (QOS)
#SBATCH --ntasks=32            # OBLIGATOIRE : doit correspondre au Mesher (32)
#SBATCH --cpus-per-task=1      # On reste simple pour éviter de bloquer des ressources
#SBATCH --time=12:00:00
#SBATCH --output=ro.txt 
#SBATCH --error=re.txt 
#SBATCH --partition=cpu_prod
#SBATCH --qos=16nodespu

module load sem3d/2024.02.22/intel-2021.9.0-intel-oneapi-mpi

mpirun -n $SLURM_NTASKS sem3d.exe > output.solver