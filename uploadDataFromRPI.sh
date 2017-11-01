#!/bin/bash
# in folder data from the sessions you want to save
# $RASPBERRY_PI_ID=ID
# sshpass -p "MonAmour" ssh -o StrictHostKeyChecking=no root@95.85.52.87

# The RPI ID will be coded in the data/ name, there

cp sessionsNames.txt dataPI*/
sshpass -p "MonAmour" scp -r dataPI* root@95.85.52.87:/root/JONRPITESTS

# sshpass enables to connect with pasword in option : -p "MonAmour" is the password
# dataP* autocomplete with the name of the PI which is not known

# https://stackoverflow.com/questions/50096/how-to-pass-password-to-scp
# We can also communicate trpugh ssh key,
# cd ~/dataOBCITesteurs
