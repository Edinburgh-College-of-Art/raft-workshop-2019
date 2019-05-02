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
cd ~
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
