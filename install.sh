#!/bin/bash

# TODO: This would all be great to have in a virtualenv

sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install python-scipy
sudo apt-get install python-opencv
sudo apt-get install python-h5py

sudo pip install keras
sudo pip install flask

# TODO: use latest instead of hard-coded tensorflow version
if [[ `which nvcc` ]]; then
    echo "Installing GPU-accelerated Tensorflow"
    export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-0.12.0rc1-cp27-none-linux_x86_64.whl
else
    echo "Installing CPU-only Tensorflow"
    export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0rc1-cp27-none-linux_x86_64.whl
fi
echo $TF_BINARY_URL
pip install $TF_BINARY_URL 
