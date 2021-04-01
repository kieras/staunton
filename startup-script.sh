#! /bin/bash

cd /opt/
apt-get -y install zip
apt-get -y install python3-venv
gsutil cp gs://staunton-source/* .
unzip -o staunton-main.zip

cd /opt/staunton-main
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt 

nohup python main.py > /opt/staunton-main/staunton.log &
