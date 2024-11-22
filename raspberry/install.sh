#!/usr/bin/env bash
sudo apt-get install libzbar-dev libzbar0
pip3 install -r ../src/rpi/requirements.txt
# https://www.digikey.com/en/maker/projects/stream-live-video-over-rtsp-from-your-raspberry-pi/e7f81253dfd443838fca109f3c1e6c92
wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.4/rtsp-simple-server_v0.21.4_linux_armv7.tar.gz
tar -xzf rtsp-simple-server_v0.21.4_linux_armv7.tar.gz
sudo mkdir /usr/local/bin/ || echo ""
sudo mv rtsp-simple-server /usr/local/bin/
sudo chmod +x /usr/local/bin/rtsp-simple-server
rtsp-simple-server
