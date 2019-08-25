#!/bin/bash

# $ pip install python-daemon
# $ pip install --upgrade google-cloud-pubsub

export GOOGLE_APPLICATION_CREDENTIALS="$( cd "$(dirname "$0")" ; pwd -P)/config/gcp-credentials.json"
python -c 'from main import main; main();'
