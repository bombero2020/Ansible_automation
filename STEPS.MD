### Pasos para desplegar la web-app en un servidor ubuntu 20.04.1 LTS 

#### Descargar la clave para conectar al servidor key.pem
```
ssh -i ubuntu-2.pem ubuntu@15.188.90.80
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
#### Migrate DDBB and Run dev server
```commandline
ansible-playbook start_the_app.yml -i inventory -l ubuntu_2 -v
```
#### Collect static files.

#### Crear super user.

### GUNICORN
#### Create service for gunicorn
#### Test gunicorn config

### NGNIX
#### Create service for nginx
#### Configure nginx
#### Test nginx config