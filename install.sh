#!/bin/bash

# TODO: This would all be great to have in a virtualenv

sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install python-scipy
sudo apt-get install python-opencv
sudo apt-get install python-h5py

sudo pip install keras
sudo pip install flask

echo Entry your hardware [GPU/CPU]
read hardware

if [[ "$hardware" == C* ]]
then
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0rc1-cp27-none-linux_x86_64.whl
  else
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-0.12.0rc1-cp27-none-linux_x86_64.whl
fi
echo $TF_BINARY_URL
pip install --upgrade $TF_BINARY_URL 
