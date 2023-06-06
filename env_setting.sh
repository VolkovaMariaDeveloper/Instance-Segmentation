#!/bin/bash

# Настройка окружения yolact
cd yolact
conda env create -f environment.yml
conda activate yolact-env
cd ../


# Настройка окружения adelai-det

git clone https://github.com/facebookresearch/detectron2.git
python -m pip install -e detectron2

cd AdelaiDet
conda env create -f environment.yml
conda activate adelai-det
python setup.py build develop
cd ../



