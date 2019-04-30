# ------------------------------------------------------------
sudo apt-get update
sudo apt-get upgrade # for the workshop we should comment this out, it takes ages otherwise
sudo apt-get install \
              nodejs \
                 npm \
       libcairo2-dev \
            puredata \
        librxtx-java \ # for processing
       openjdk-6-jdk \ # for processing
       netatalk \ # for viewing files on OS X filesystem
# ------------------------------------------------------------
# Install Processing
curl https://processing.org/download/install-arm.sh | sudo sh

# ------------------------------------------------------------
# Bluetooth
cd ~
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
tar -xf bluez-5.37.tar.xz
cd bluez-5.37
sudo apt-get install -y \
             libusb-dev \
          libdbus-1-dev \
         libglib2.0-dev \
            libudev-dev \
            libical-dev \
        libreadline-dev \
            python-dbus \
         python-gobject \
              bluetooth \
                  bluez \
                blueman \
           pi-bluetooth \
           python-bluez

./configure
make
sudo make install

# cat "PRETTY_HOSTNAME=RaspberryPi" >> /etc/machine-info # Set Peripheral Name

sudo systemctl start bluetooth
systemctl status bluetooth
sudo systemctl stop bluetooth

# OR

sudo pip3 install bluepy
# ------------------------------------------------------------
# I2C
sudo apt-get install -y \
           python-smbus \
              i2c-tools

# ------------------------------------------------------------
# Python OSC
pip3 install python-osc
git clone https://github.com/toddtreece/osc-examples.git
cd osc-examples
npm install
cd ..
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
