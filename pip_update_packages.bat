
pip freeze > upgrade_requirements.txt

pip install -r upgrade_requirements.txt  --upgrade

del upgrade_requirements.txt

