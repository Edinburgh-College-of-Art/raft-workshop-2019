<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. OS install to SD card</a>
<ul>
<li><a href="#sec-1-1">1.1. format micro SD card using NOOBS</a></li>
</ul>
</li>
<li><a href="#sec-2">2. do what follows with an ethernet cable serving a DHCP address to the raspberry pi that's connected to the internet</a>
<ul>
<li><a href="#sec-2-1">2.1. enable VNC server</a></li>
<li><a href="#sec-2-2">2.2. set WIFI country</a></li>
<li><a href="#sec-2-3">2.3. enable ssh</a></li>
<li><a href="#sec-2-4">2.4. take note of your WIFI mac address:</a></li>
<li><a href="#sec-2-5">2.5. which Router</a></li>
<li><a href="#sec-2-6">2.6. enable netatalk</a></li>
<li><a href="#sec-2-7">2.7. enable l2c in rasberry pi settings</a></li>
<li><a href="#sec-2-8">2.8. install pythonOSC</a></li>
<li><a href="#sec-2-9">2.9. make sure that wifi is working and that you've setup the network you want it to connect to</a></li>
<li><a href="#sec-2-10">2.10. install pure data</a></li>
<li><a href="#sec-2-11">2.11. get IP addresses of all computers on your network</a></li>
<li><a href="#sec-2-12">2.12. install LSM303</a></li>
<li><a href="#sec-2-13">2.13. make the Pi run your code on load</a></li>
<li><a href="#sec-2-14">2.14. copying install</a></li>
</ul>
</li>
<li><a href="#sec-3">3. Jobs to do</a>
<ul>
<li><a href="#sec-3-1">3.1. the struggle between our desire to intervene (led by taste) and the obligation to leave things to sit still and do what they have to do</a></li>
</ul>
</li>
</ul>
</div>
</div>


# OS install to SD card<a id="sec-1" name="sec-1"></a>

***!!!!!NOTE, do not try to install the OS from battery, plug into a wall wart supplying consistent 5v 2 amp minimum so that the OS can install, it simply flakes out every time otherwise. !!!!!***  

## format micro SD card using NOOBS<a id="sec-1-1" name="sec-1-1"></a>

Download latest NOOBS
<https://www.raspberrypi.org/downloads/noobs/>

You'll probably want to download and install the SD card formatter they recommend:
<https://www.sdcard.org/downloads/formatter_4/>

Copy across the unzipped noobs stuff and go with the standard install instructions from here:
<https://www.raspberrypi.org/help/noobs-setup/2/>

# do what follows with an ethernet cable serving a DHCP address to the raspberry pi that's connected to the internet<a id="sec-2" name="sec-2"></a>

## enable VNC server<a id="sec-2-1" name="sec-2-1"></a>

`pi icon in top left >preferences >raspberry pi configuration`
enable VNC server.
When this is enabled, go to options and in security set VNC password to be on, when you hit apply, it will prompt you to add a password, do so.

## set WIFI country<a id="sec-2-2" name="sec-2-2"></a>

Important to set the WIFI country or wifi won't work
Do this in the location settings

## enable ssh<a id="sec-2-3" name="sec-2-3"></a>

Again doable in the screen-based pi configuration settings, navigate to here 
`pi icon in top left >preferences >raspberry pi configuration`
Enable SSH

## take note of your WIFI mac address:<a id="sec-2-4" name="sec-2-4"></a>

`ls /sys/class/net`
returns the mac address of your machine

`ls /sys/class/net > macAddressWifi.txt`
writes the line to a text file

The above is useful as you can keep a log of all the mac address of your many pis and copy paste the text to your router if you want to make sure the router serves specific addresses to EACH PI.

## which Router<a id="sec-2-5" name="sec-2-5"></a>

I'm using a master control router
SSID sonikebana
PS citys0unds

## enable netatalk<a id="sec-2-6" name="sec-2-6"></a>

This means you can see your pi's directory and write to it from OS X, very useful for transferring files to it. Transfer large audio files with the ethernet cable attached. 

-   `sudo apt-get install netatalk`
-   `sudo /etc/init.d/netatalk stop`
-   `sudo nano /etc/netatalk/AppleVolumes.default`

-You can edit the mount folder if you wish or leave the default value: ~/ "Home Directory”
-Start the service again
-   `sudo /etc/init.d/netatalk start`

## enable l2c in rasberry pi settings<a id="sec-2-7" name="sec-2-7"></a>

check compass is connected
`sudo i2cdetect -y 1`
Make sure that you've also added these lines to /etc/modules
`sudo nano /etc/modules`
`i2c-bcm2708`
`i2c-dev`

<https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/overview>
<https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c>
<https://github.com/adafruit/Adafruit_Python_LSM303>

NOTE it's very important that you install for python 3 in this case, when all the github stuff is done

`sudo python3 setup.py install`

## install pythonOSC<a id="sec-2-8" name="sec-2-8"></a>

`pip3 install python-osc`

## make sure that wifi is working and that you've setup the network you want it to connect to<a id="sec-2-9" name="sec-2-9"></a>

SSID - GL-AR300M-93c
PW - goodlife

## install pure data<a id="sec-2-10" name="sec-2-10"></a>

`sudo apt-get install pure data`

## get IP addresses of all computers on your network<a id="sec-2-11" name="sec-2-11"></a>

`arp -a`

install adafruit GPIO stuff
sudo apt-get install python-rpi.gpio

## install LSM303<a id="sec-2-12" name="sec-2-12"></a>

sudo apt-get install git build-essential python-dev
cd ~
git clone <https://github.com/adafruit/Adafruit_Python_LSM303.git>
cd Adafruit<sub>Python</sub><sub>LSM303</sub>
sudo python setup.py install

## make the Pi run your code on load<a id="sec-2-13" name="sec-2-13"></a>

To do this, you'll need to edit your ~/.profile file
At the end of this file, link to your launcher script. 
I'm using the following script

    #!/bin/sh
    
    #  sonikebanaLaunch.sh
    #  
    #
    #  Created by PARKER Martin on 03/04/2018.
    #
    (sleep 15 && python3 ~/Desktop/sonikebana/lsm303_to_pd.py) &
    (sleep 5 && puredata ~/Desktop/sonikebana/_main.pd) &
    exit 0

## copying install<a id="sec-2-14" name="sec-2-14"></a>

<https://raspberrypi.stackexchange.com/questions/311/how-do-i-backup-my-raspberry-pi>

On the Mac you don't want to be using /dev/diskn. You should use /dev/rdiskn instead, where n is the number the OS uses to identify your SD card. This decreases the time required to copy by a huge amount.

So for the optimal backup process on a Mac, I would recommend doing the following:

Run diskutil list, and find the disk corresponding to your Raspberry Pi's SD card:

$ diskutil list
/dev/disk0
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID<sub>partition</sub><sub>scheme</sub>                        \*500.1 GB   disk0
   1:                        EFI                         209.7 MB   disk0s1
   2:                  Apple<sub>HFS</sub> Macintosh HD            499.2 GB   disk0s2
   3:                 Apple<sub>Boot</sub> Recovery HD             650.0 MB   disk0s3
/dev/disk1
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk<sub>partition</sub><sub>scheme</sub>                        \*7.9 GB     disk1
   1:             Windows<sub>FAT</sub><sub>32</sub>                         58.7 MB    disk1s1
   2:                      Linux                         7.9 GB     disk1s2

Clearly /dev/disk1 is my 8GB SD card, the Linux partition name is also a bit of a clue.

However, instead of using /dev/disk1 with dd, you should use /dev/rdisk1, like so:

sudo dd if=/dev/rdisk1 of=/path/to/backup.img bs=1m

And to restore it, just swap the if (input file), and of (output file) parameters:

sudo dd if=/path/to/backup.img of=/dev/rdisk1 bs=1m

Or, with gzip, to save a substantial amount of space:

sudo dd if=/dev/rdisk1 bs=1m | gzip > /path/to/backup.gz

And, to copy the image back onto the SD:

gzip -dc /path/to/backup.gz | sudo dd of=/dev/rdisk1 bs=1m


