#!/bin/bash
sudo date --set 2017-10-10
curl -sL https://deb.nodesource/setup_8.x | sudo -E bash -
sudo apt install nodejs

sudo apt-get -y purge wolfram-engine
sudo apt-get -y purge libreoffice
sudo aptitude hold wolfram-engine
sudo aptitude hold libreoffice
# sudo apt update
# sudo apt -y full-upgrade
sudo apt-get -y install Bluetooth
sudo apt-get -y install blueman
sudo apt-get -y install bluez
sudo apt-get -y install libbluetooth-dev
sudo apt-get -y install python-numpy python-scipy python-pandas python-pyaudio
sudo pip install colour
cd ~/Desktop
mkdir v011
cd v011
git clone -b v011 https://github.com/zeta-technologies/tests-raspberry
cd tests-raspberry/OBGanglion
npm install
npm install lodash
npm install clone
