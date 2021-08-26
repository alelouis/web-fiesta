#!/bin/bash
conda init bash
source ~/.bashrc
conda activate fiesta
gunicorn -b 0.0.0.0:5000 -k eventlet api:app
