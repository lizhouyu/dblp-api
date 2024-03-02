# Customized DBLP API

![version-0.2.1](https://img.shields.io/badge/version-0.2.1-blue)
![python->=3.10](https://img.shields.io/badge/python->=3.10-blue?logo=python&logoColor=white)
![license-MIT](https://img.shields.io/badge/license-MIT-green)

Customized based on [dblp-api](https://github.com/alumik/dblp-api).

A helper package to get information of scholarly articles from [DBLP](https://dblp.uni-trier.de/) using its public API.

## Pre-requisites
* Anaconda or Miniconda: [Installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

## Environment setup

```bash
conda env create -f environments.yml
```

```bash
conda activate dblp
```

## Usage example

```bash
python search.py -q "smart home" -y 2023 2022 2021 -c A
```
Results will be saved in `results_smart_home_2023_2022_2021_A.txt`.
