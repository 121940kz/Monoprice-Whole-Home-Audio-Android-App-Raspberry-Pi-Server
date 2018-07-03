# Monoprice Whole Home Audio Android App Raspberry Pi Server
For use with the Monoprice 6 zone 6 source OR Dayton Audio DAX66 amplifiers...This python script which turn your raspberry pi into a TCP server accepting connections from the [Monopice Whole Home Audio Android App by TheKMZ1 in the google play store](https://play.google.com/store/apps/details?id=com.monoprice.audiocontrol&hl=en_US). You will need a USB to Serial Cable plugged into your Pi/amp. 

## Prerequisite
You need a raspberry pi (any model) that has a distribution of linux on it. I used [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
I am working under the assumption that you alreday have your raspberry pi setup and running, this is not a guide on how to install raspbian on your pi.
Your raspberry pi needs python installed. By deault, Raspbian already has python installed, but in case you don't have it, install it by issuing this command `sudo apt-get install python3-picamera`

## Installation Steps
1) Log into your Raspberry Pi, and navigate to `/bin` normally at the command line you are in the user folder, so issuing `cd ../../bin` will take you back 2 directories and into the bin folder
2) Once you are in `/bin` issue the command to download the python file `wget `
3) We want this server to always be running, so in the event the Raspberry Pi reboots, we want it to automatically start up again. Inside of the `/etc` folder edit the rc.local file by typing `sudo nano rc.local`
4) At the bottom right above `exit 0`, add `python ../bin/MonopriceAudioPythonServer.py &` use `CTRL X` and then `Y` to save the file
