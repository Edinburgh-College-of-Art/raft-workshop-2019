# ------------------------------------------------------------
# sudo apt-get update
# sudo apt-get upgrade # for the workshop we should comment this out, it takes ages otherwise
sudo apt-get install -y \
        python-rpi.gpio \
       python3-rpi.gpio
# ------------------------------------------------------------       
sudo apt-get install \
              nodejs \
                 npm \
       libcairo2-dev \
            puredata \
        librxtx-java \ # for processing
       openjdk-6-jdk \ # for processing
            netatalk  # for viewing files on OS X filesystem
# ------------------------------------------------------------
# Optionally add installation of some useful multimedia packages 
# uncomment the following by deleting the hash before running the script. 

# sudo apt-get install sox # smash up some sound files
# sudo apt-get install ffmpeg # do anything you like to video
# sudo apt-get install mpv # a really nice video player
# Install Processing
# curl https://processing.org/download/install-arm.sh | sudo sh
cd ~
# ------------------------------------------------------------
# # Bluetooth
# cd ~
# wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
# tar -xf bluez-5.37.tar.xz
# cd bluez-5.37
# sudo apt-get install -y \
#              libusb-dev \
#           libdbus-1-dev \
#          libglib2.0-dev \
#             libudev-dev \
#             libical-dev \
#         libreadline-dev \
#             python-dbus \
#          python-gobject \
#               bluetooth \
#                   bluez \
#                 blueman \
#            pi-bluetooth \
#            python-bluez
#
# ./configure
# make
# sudo make install
#
# # cat "PRETTY_HOSTNAME=RaspberryPi" >> /etc/machine-info # Set Peripheral Name
#
# sudo systemctl start bluetooth
# systemctl status bluetooth
# sudo systemctl stop bluetooth
#
# # OR
#
# sudo pip3 install bluepy
# ------------------------------------------------------------
# I2C
sudo apt-get install -y \
           python-smbus \
              i2c-tools

# ------------------------------------------------------------
# Python OSC
curl -sL https://deb.nodesource.com/setup_10.x > nodesetup.sh
sudo bash nodesetup.sh
sudo apt-get install -y nodejs

pip3 install python-osc
git clone https://github.com/toddtreece/osc-examples.git
cd osc-examples
npm install
cd ~
# ------------------------------------------------------------
# lsm303
sudo pip3 install adafruit-lsm303
# ------------------------------------------------------------
# Grove Sensors
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .
cd ..
# python3 examples/blink.py
# ------------------------------------------------------------
# stop and restart netatalk
sudo /etc/init.d/netatalk stop
sudo /etc/init.d/netatalk start
# ------------------------------------------------------------
# set the main preferences for the operating system such as vnc, ssh i2c etc. 
sudo raspi-config nonint do_ssh 0 # turn on SSH
sudo raspi-config nonint do_vnc 0 # turn on VNC
sudo raspi-config nonint do_i2c 0 # turn on i2c interface
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial 0 
sudo raspi-config nonint do_rgpio 0
sudo raspi-config nonint do_resolution 1920 1080 # set the monitor resolution so that when you VNC in, it's not a tiny shitty screen
