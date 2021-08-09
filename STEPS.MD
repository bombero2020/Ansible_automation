### Pasos para desplegar la web-app en un servidor ubuntu 20.04.1 LTS 

#### Descargar la clave para conectar al servidor key.pem
```
ssh -i ubuntu-2.pem ubuntu@15.188.81.240
```
#### Paso 1: crear usuario marcelo con permisos de root.

```commandline
ansible-playbook create_sudoer_user.yml -i inventory -l ubuntu_2 -v
```
#### Instalar NGINX
```commandline
ansible-playbook install_nginx.yml -i inventory -l ubuntu_2 -v
```
#### Instalar venv para el proyecto
```commandline
ansible-playbook install_venv.yml -i inventory -l ubuntu_2 -v
```
#### Copiar la Base de datos
```commandline
ansible-playbook create_db_directory.yml -i inventory -l ubuntu_2 -v
```
#### Desplegar la app desde github
```commandline
ansible-playbook deploy_app_from_github.yml -i inventory -l ubuntu_2 -v
```
#### Instalar requirements (en el venv)
```commandline
ansible-playbook install_venv_requirements.yml -i inventory -l ubuntu_2 -v
```

#### Orquestador: Todos los pasos de arriba en un solo playbook

```commandline
ansible-playbook orquestrate.yml -i inventory -l ubuntu_2 -v
```

### DJANGO
#### Migrate DDBB and Run dev server, Collect static files.
```
ansible-playbook start_the_app.yml -i inventory -l ubuntu_2 -v
```

#### Crear super user. todo

### GUNICORN
#### Create service for gunicorn
```
ansible-playbook copy_gunicorn_service.yml -i inventory -l ubuntu_2 -v
```
#### Test gunicorn config
test con curl usando el socket:
```
curl --unix-socket /run/gunicorn.sock localhost
```

#### Comando para generar passwd:
```commandline
openssl rand -base64 32
```

### NGNIX
#### Configure nginx
```
ansible-playbook configure_nginx.yml -i inventory -l ubuntu_2 -v
```
#### Test nginx config
```
sudo nginx -t
```
### SSL Certificates
```
ansible-playbook install_ssl_cerbot.yml -i inventory -l ubuntu_2 -v -t paso2
```