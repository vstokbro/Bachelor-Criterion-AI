#!/bin/sh
#BSUB -J version00001
#BSUB -o version00001%J.out
#BSUB -q gpuv100
#BSUB -n 1
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=32G]"
#BSUB -R "select[gpu32gb]"
#BSUB -W 24:00
#BSUB -u s173934@win.dtu.dk
#BSUB -N
# end of BSUB options

echo "Running script..."
cd ..
source test-env/bin/activate
cd Bachelor-Criterion-AI
python3 semantic_segmentation/DeepLabV3/experiment_generator.py 0.01 DeepLab RMS optim_exp optimizer/RMS
python3 semantic_segmentation/DeepLabV3/experiment_generator.py 0.01 MobileNet Rms optim_exp optimizer/RMS
echo "Done"