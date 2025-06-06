conda create --name test_env --file ./requirements.txt -c conda-forge -y
conda activate test_env
python -m ipykernel install --user --name test_env
