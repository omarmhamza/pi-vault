echo "Starting Installation"
pip install -r ../requirements.txt
python create_key.py
python migrate.py
echo "Installation Successful"
