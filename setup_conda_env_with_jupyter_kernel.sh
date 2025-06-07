conda create --name rb87_detection_env --file ./requirements.txt -c conda-forge -y
conda activate rb87_detection_env
python -m ipykernel install --user --name rb87_detection_env
