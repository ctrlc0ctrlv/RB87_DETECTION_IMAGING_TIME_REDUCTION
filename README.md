# RB87_DETECTION_IMAGING_TIME_REDUCTION

<!-- <img src="./src/image.png" width="800"/>  -->
<!-- TODO: fix image -->

## 1. About the project

Single neutral atoms $\left( ^{87}\text{Rb},\ ^{133}\text{Cs},\ ^{87}\text{Sr} \right)$ are one of the promising architectures for creating quantum computers. Individual atoms captured in an array of static tweezers (traps) are used as carriers of qubits (quantum bits), the glow signal from which can be obtained using a light-sensitive camera during the exposure time $T_\text{exp}$.

The project is devoted to methods methods for fast and high-quality determination of the absence/presence of an atom at a known point in an image - “atom detection”. As detection algorithms, we consider a threshold classifier, a Bayesian classifier and a convolutional neural network (CNN).

The main difficulty of the detection - the only experimental data avaliable is the trap array images: <ins>no any labels are avaliable</ins>. To overcome this issue, we utilize the "three-images measurement scheme" [Phuttitarn et al., 2024]. Three consecutive images $\mathcal{I}_{1, 2, 3}$ are obtained using the large-small-large exposure time values. Then, by classifying images $\mathcal{I}_{1, 3}$ and comparing their labels, we can get $\mathcal{I}_2$ labels.

Current repository includes a few Jupyter notebooks with data processing, three detectors training and comparison the results on data test subset.

## 2. Data

The raw self-collected dataset (images + trap array positions of the enabled traps) can be obtained via [GoogleDrive link](https://drive.google.com/file/d/16zwKv0SIk-mxchAcTJvKGfch5xH2q0u-/view?usp=sharing)

## 3. Setup

### 3.1. If you're planning to use the raw data

1. Download the raw data on the link above
2. Extract the .zip archive contents to the `./data/raw` folder. The path to the images should look like this: `/path/to/current/directory/data/raw/rb3.2_2197950934861us_third_14999.png`

### 3.2. If the raw data is not needed

1. You don't have to do anything manually - the preprocessed data can be found in `/path/to/current/directory/data/preprocessed`

### 3.3. Environment setup

Prefer using `conda` over than `pip` to avoid packages conflicts

Run script `setup_test_env_with_jupyter_kernel.sh` to install the conda `test_env` environment with all required dependencies (based on `requirements.txt`). Also this script adds new Jupyter kernel, so that the Jupyter notebook could be executed (tested on both Jupyter Lab and Visual Studio Code).

You can also use `requirements.txt` to install all the packages using `pip`, but good performance is not guaranteed.

## 3. Acknowledgements

**This work was supported by Non-commercial Foundation for the Advancement of Science and Education INTELLECT.**

Also thanks to <https://github.com/Nikita-Belyakov> for productive consultations during the work on the project.
