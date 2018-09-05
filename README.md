# Unbiased Clustering Pipeline

This project was implemented in [Itay Tirosh Lab](http://www.weizmann.ac.il/mcb/tirosh/).

In this project we implement unbiased clustering for cell lines as was described in [Puram et al., Single-Cell Transcriptomic Analysis of Primary and Metastatic Tumor Ecosystems in Head and
Neck Cancer, Cell (2018)](https://www.ncbi.nlm.nih.gov/pubmed/29198524).

The main file is `CellLineWork/ExpressionAnalysis.py` which runs a preprocessing pipeline for cell line expression profiles. 
The pipeline performs clustering as well.

## Directories
### 1. CellLineWork
This folder contains files unique to work on cell line expression data. It utilizes other folders and main files are located in it.

### 2. PreprocessingPipeline
This folder contains a skeleton pipeline for single cell expression profiles. It can be used for multiple purposes and new transformations can be added to it.

### 3. jupyter_analyses
This folder contains post clustering analyses of cell line single cell expression profiles.
