# Monoprice Whole Home Audio Android App Raspberry Pi Server
For use with the Monoprice 6 zone 6 source OR Dayton Audio DAX66 amplifiers...This python script which turn your Raspberry Pi into a TCP server accepting connections from the [Monopice Whole Home Audio Android App by TheKMZ1 in the google play store](https://play.google.com/store/apps/details?id=com.monoprice.audiocontrol&hl=en_US). 

You will need a USB to Serial Cable plugged into your Pi/amp. 

## Prerequisite
You need a Raspberry Pi (any model) that has a distribution of linux on it. I used [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

I am working under the assumption that you alreday have your raspberry pi setup and running, this is not a guide on how to install raspbian on your Pi. You also need it on your local network, and static IP address is strongly recommended. You can either have your raspberry pi plugged in with an ethernet cable, or join it to your wireless network if you have Wi-Fi on your Pi. 

Your Raspberry Pi needs python installed. By deault, Raspbian already has python installed, but in case you don't have it, install it by issuing this command `sudo apt-get install python3-picamera`

## Quick Install Steps
1) Navigate to `/bin` directory on the Pi
2) Use `wget ` to download the python server file into that directory
3) Navigate to `/etc` directory
4) Edit the `rc.local` file
5) At the bottom before exit 0, add `python ../bin/MonopriceAudioPythonServer.py &`
6) Save the file
7) Reboot the Pi to see if the server is up and running and that the android app works
8) If it doesn't work, refer to the troubleshooting steps

## Detailed Install Steps
1) Log in/SSH into your Raspberry Pi, and navigate to the `/bin` directory. Normally when you first SSH in, the command lineplaces you in the user folder, so issuing `cd ../../bin` will take you back 2 directories and into the bin folder. If it doesn't, then the easiest way is to just continue to issue `cd ..` until you cannot go back any more directories, and then finally issue `cd /bin`.

2) Once you are in the `/bin` directory, issue the command to download the python file into that folder `wget `

3) We want this server to always be running, so in the event the Raspberry Pi reboots, we want it to automatically start up again. Inside of the `/etc` folder edit the rc.local file by typing `sudo nano rc.local`

4) At the bottom right above `exit 0`, add `python ../bin/MonopriceAudioPythonServer.py &` use `CTRL X` and then `Y` to save the file

## Troubleshooting If Not Working

#### All the steps worked but the android app doesn't work / isn't connecting to it
If you performed all the steps and the app isn't working, it is best to comment out the the line in the `rc.local` file that was added in step 4, and try to run the python file manually.  

#### Some of the steps above failed

