# How to Boot raspberry from start :



Mount the sd card with the right image (that's very important) : `2016-09-23-raspbian-jessie.img`
 Then different commands to run to boot the raspberry :

 `diskutil list `
 `diskutil unmountDisk /dev/<disk # from diskutil>`

`sudo dd bs=1m if=<image.img> of=/dev/rdisk<disk# from diskutil>
`

 # On the Raspberry Pi terminal:
 `git clone -b <branch_Name> https://schmustach@bitbucket.org/zeta-technologies/tests-raspberry.git`
 then :
`cd tests-raspberry`
 and `./openbciSetup.sh`


# Save data from the raspberry to Digital Ocean droplet:

Look at the file uploadDataFromRPI.sh, check that the path of the data to copy is the good one, and the destination is good as well, by default it copies to
/root/dataOBCITesteurs on the droplet.
Make sure the paths are right in the file `uploadDataFromRPI.sh`
Make sure you `chmod +x uploadDataFromRPI`
