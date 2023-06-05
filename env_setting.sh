#!/bin/bash

# Настройка окружения yolact
cd yolact
conda env create -f environment.yml
conda activate yolact-env
cd ../

# Настройка окружения adelai-det
cd yolact
conda env create -f environment.yml
conda activate adelai-det
cd ../


