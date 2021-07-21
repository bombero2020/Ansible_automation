### Pasos para desplegar la web-app en un servidor ubuntu 18.04.1 LTS 

#### Descargar la clave para conectar al servidor key.pem
```buildoutcfg
ssh -i ubuntu-2.pem ubuntu@35.181.57.16
```
#### Paso 1: crear usuario marcelo con permisos de root.
```
ansible-playbook create_sudoer_user.yml -i inventory -l ubuntu_2 -v
```
#### Instalar NGINX
```buildoutcfg
ansible-playbook install_nginx.yml -i inventory -l ubuntu_2 -v
```
#### Instalar Gunicorn

#### Instalar Django
