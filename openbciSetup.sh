#!/bin/bash
sudo date --set 2017-11-01
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt-get -y install sshpass
sudo apt-get -y purge wolfram-engine
sudo apt-get -y purge libreoffice
sudo aptitude -y hold wolfram-engine
sudo aptitude -y hold libreoffice
sudo apt-get -y install Bluetooth
sudo apt-get -y install blueman
sudo apt-get -y install bluez
sudo apt-get -y install libbluetooth-dev
sudo apt-get -y install python-numpy
sudo apt-get -y install python-scipy
sudo apt-get -y install python-pandas
sudo apt-get -y install python-pyaudio
sudo pip install colour
cd ~/Desktop/v011/tests-raspberry/OBGanglion
npm install lodash
npm install clone
npm install
