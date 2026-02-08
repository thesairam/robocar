
To create a service
sudo nano /etc/systemd/system/robo-web.service

to start and enable the service on boot

sudo systemctl daemon-reload 
sudo systemctl enable robo-web.service
sudo systemctl start robo-web.service