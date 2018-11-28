#!/bin/sh

sudo apt-get install python3-pip
pip3 install -r requirements.txt
pip3 install --user cozmo[3dviewer]
sudo apt-get install freeglut3-dev
