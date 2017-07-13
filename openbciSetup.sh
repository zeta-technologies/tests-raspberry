#!/bin/bash
sudo apt update && sudo apt full-upgrade
wget --quiet -O - https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt install nodejs
sudo apt-get install npm
npm install openbci-ganglion lodash clone
sudo apt-get install Bluetooth bluez-utils blueman
sudo apt-get install python-gobject python-gobject-2 libbluetooth-dev python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose python-pyaudio
