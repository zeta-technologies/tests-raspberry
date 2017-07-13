#!/bin/bash
sudo apt -y update
sudo apt -y full-upgrade
wget --quiet -O - https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt-get -y install npm
sudo apt-get -y install Bluetooth bluez-utils blueman bluez python-gobject python-gobject-2
sudo apt-get -y install libbluetooth-dev
sudo apt-get -y install python-numpy python-scipy python-matplotlib python-pandas python-sympy python-nose
sudo apt-get -y install python-pyaudio
npm install openbci-ganglion
npm install lodash
npm install clone
sudo reboot
