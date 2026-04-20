
#!/usr/bin/env bash

apt-get update

# Required for sklearn & numpy
apt-get install -y build-essential
apt-get install -y libatlas-base-dev

# Tesseract for OCR
apt-get install -y tesseract-ocr

pip install --upgrade pip
pip install -r requirements.txt

