#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=02-00:00:00
#SBATCH --job-name=spotify
#SBATCH --gpus-per-task=2
#SBATCH --mem-per-cpu=4096
#SBATCH --mail-type=ALL
#SBATCH --mail-user=prateek.pani@research.iiit.ac.in


module load cuda/10.0
module load cudnn/7.6-cuda-10.0

python mk_p2s.py
