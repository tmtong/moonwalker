sudo apt-get install rpi.gpio
sudo groupadd gpio
sudo usermod -a -G gpio tmtong
sudo grep gpio /etc/group
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
# log out and log in
pip install roslibpy ros-foxy-rosbridge-suite
# dont forget to turn on the battery for the motor


