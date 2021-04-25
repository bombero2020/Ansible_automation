Tutorial:
Para ubuntu 20:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04-es
Para ubuntu 16.04.
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

`Crear un entorno virtual:`
python -V
output: Python 3.8.6
python -m virtualenv venv

Requirements:
pip install django==3.1.3 gunicorn==20.0.4

test gunicorn:
gunicorn --bind 0.0.0.0:8000 Dulcesyto.wsgi

Crear unix socket para gunicorn:
sudo nano /etc/systemd/system/gunicorn.socket
###########################
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

###########################

Crear service para gunicorn:
sudo nano /etc/systemd/system/gunicorn.service
###########################
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=marcelo
Group=www-data
WorkingDirectory=/home/marcelo/github_projects/Dulcesyto
ExecStart=/home/marcelo/github_projects/Dulcesyto/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          Dulcesyto.wsgi

[Install]
WantedBy=multi-user.target

###########################
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn.service
sudo journalctl -u gunicorn.socket
sudo journalctl -u gunicorn.service

curl --unix-socket /run/gunicorn.sock localhost

###### NGINX
sudo nano /etc/nginx/sites-available/Dulcesyto
########################
server {
    listen 80;
    server_name 192.168.188.129;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/marcelo/github_projects/Dulcesyto;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
########################
sudo ln -s /etc/nginx/sites-available/Dulcesyto /etc/nginx/sites-enabled

sudo nginx -t
sudo systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

`Pendiente SSL/TLS`

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/github_projects/Dulcesyto
ExecStart=/home/ubuntu/github_projects/Dulcesyto/venv/bin/gunicorn \
          --access-logfile /home/ubuntu/acces-log-gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/github_projects/Dulcesyto/Dulcesyto.sock \
          Dulcesyto.wsgi

[Install]
WantedBy=multi-user.target
