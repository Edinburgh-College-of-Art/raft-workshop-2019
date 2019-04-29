# ------------------------------------------------------------
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install \
              nodejs \
                 npm \
       libcairo2-dev \
            puredata \
        librxtx-java \ # for processing
       openjdk-6-jdk \ # for processing
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
        libreadline-dev

./configure
make
sudo make install

systemctl status bluetooth

# OR

pip install bluepy
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
python3 examples/blink.py
# ------------------------------------------------------------
# install Pure Data
sudo apt-get install puredata
# ------------------------------------------------------------
