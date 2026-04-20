#!/usr/bin/env bash

# install tesseract
apt-get update
apt-get install -y tesseract-ocr

pip install -r requirements.txt
