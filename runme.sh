#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="$( cd "$(dirname "$0")" ; pwd -P)/config/gcp-credentials.json"
python main.py
