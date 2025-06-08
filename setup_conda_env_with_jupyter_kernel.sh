conda create --name rb87_detection_env --file ./requirements.txt -c conda-forge -y
conda init --all
exec $SHELL
source activate rb87_detection_env
conda activate rb87_detection_env
python -m ipykernel install --user --name rb87_detection_env
