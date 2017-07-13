#!/bin/bash
sudo apt update --forces -yes
sudo apt full-upgrade --forces-yes
wget --quiet -O - https://deb.nodesource.com/setup_8.x --forces-yes | sudo -E bash - --forces-yes
sudo apt install nodejs --forces-yes
sudo apt-get install npm --forces-yes
npm install openbci-ganglion lodash clone --forces-yes
sudo apt-get install Bluetooth bluez-utils blueman bluez python-gobject python-gobject-2
sudo apt-get install libbluetooth-dev
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose --forces-yes
sudo apt-get install python-pyaudio
