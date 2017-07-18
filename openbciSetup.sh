#!/bin/bash
sudo apt-get clean
sudo apt-get autoremove
sudo apt-get -y purge wolfram-engine
sudo apt-get -y purge libreoffice
sudo aptitude hold wolfram-engine
sudo aptitude hold libreoffice
sudo apt update
sudo apt -y full-upgrade
wget --quiet -O - https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt-get -y install npm
sudo apt-get -y install Bluetooth bluez-utils blueman bluez python-gobject python-gobject-2
sudo apt-get -y install libbluetooth-dev
sudo apt-get -y install python-numpy
sudo apt-get -y install python-scipy
sudo apt-get -y install python-pandas
# sudo apt-get -y install python-sympy
# sudo apt-get -y install python-nose
sudo apt-get -y install python-pyaudio
npm install openbci-ganglion
npm install lodash
npm install clone
