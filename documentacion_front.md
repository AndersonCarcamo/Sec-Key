## Paleta de Colores
Color Primario: #4A90E2 (Azul)
Color Secundario: #50E3C2 (Verde)
Color de Fondo: #F5F7FA (Gris claro)
Color de Texto Principal: #333333 (Gris oscuro)
Color de Texto Secundario: #7F8C8D (Gris medio)
Color de Botón Principal: #8E44AD (Morado)
Color de Botón Secundario: #3498DB (Azul Claro)

## para el usuo de video en vivo

### instalacion de librerias

``` shell
sudo apt update
sudo apt install -y nginx libnginx-mod-rtmp
```

La configuracion se puede ver en: /etc/nginx (linux)

sudo nano /etc/nginx/nginx.conf
sudo gedit /etc/nginx/nginx.conf
sudo gedit /etc/nginx/sites-enabled/default

sudo systemctl restart nginx

ver logs de accesos:
sudo tail -f /var/log/nginx/access.log


Configurar el puerto para que funcione correctamente

ver el estado de nginx:

sudo systemctl status nginx


para usar la camara del sistema:
ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -f flv rtmp://localhost:1935/live/stream