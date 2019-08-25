#!/bin/bash

#//  $ pip install python-daemon
#//  $ pip install --upgrade google-cloud-pubsub
#//  $ pip install pathlib2

#//  $ sudo mkdir /opt/sensor-datafile
#//  $ sudo chown $(id -un).$(id -gn) /opt/sensor-datafile
#//  $ mkdir /opt/sensor-datafile/node-0001/
#//  $ mkdir /opt/sensor-datafile/node-0001/source/
#//  $ mkdir /opt/sensor-datafile/node-0001/processing/
#//  $ mkdir /opt/sensor-datafile/node-0001/error/
#//  $ mkdir /opt/sensor-datafile/node-0001/archive/


export GOOGLE_APPLICATION_CREDENTIALS="$( cd "$(dirname "$0")" ; pwd -P)/config/gcp-credentials.json"
python main.py
