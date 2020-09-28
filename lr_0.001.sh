#!/bin/sh
#BSUB -J version001
#BSUB -o version001%J.out
#BSUB -q gpuv100
#BSUB -n 2
#BSUB -gpu "num=2:mode=exclusive_process"
#BSUB -R "rusage[mem=32G]"
#BSUB -R "select[gpu32gb]"
#BSUB -R "span[hosts=1]"
#BSUB -W 24:00
#BSUB -u s173934@win.dtu.dk
#BSUB -N
# end of BSUB options

echo "Running script..."
cd ..
source test-env/bin/activate
cd Bachelor-Criterion-AI
python3 semantic_segmentation/DeepLabV3/dataloader.py
echo "Done"