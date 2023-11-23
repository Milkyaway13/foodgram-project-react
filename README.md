# Проект «Продуктовый помощник» - Foodgram
Foodgram - Продуктовый помощник. Сервис предназначен для создания и публикации рецептов. Вы можете оформлять подписку на других пользователей. Понравившиеся рецепты можно добавить себе  "Избранное", а также в корзину, чтобы скачивать список продуктов, необходимых для приготовления различных блюд.

## Технологический стек
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)


## Как развернуть проект на сервере:


Войдите на свой удаленный сервер и обновите индекс пакетов APT:
```
sudo apt update
```
Обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```
На сервере в редакторе nano откройте конфиг Nginx:
```
nano /etc/nginx/sites-enabled/default 
```
Измените настройки location в секции server:
```
server {
    server_name <your_server_name>;
    root /var/www/foodgram/;
    location / {
      proxy_set_header Host $http_host;
      proxy_pass http://127.0.0.1:<you_working_port>;
      client_max_body_size 20M;
    }

```
Проверьте конфигурацию конфига и перезагрузите его
```
sudo nginx -t
```
```
sudo service nginx reload
```
Скопируйте подготовленные файлы `docker-compose.production.yml`:
```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
```
На сервере в папке foodgram создайте файл .env и заполните его данными
```
touch .env
nano .env

SECRET_KEY=<SECRET_KEY>
DB_NAME=<DB_NAME>
POSTGRES_USER=<USER>
POSTGRES_PASSWORD=<PASSWORD>
DB_HOST=<HOST>
DB_PORT=<PORT>
DB_NAME=<DB_NAME>
DEBUG=<VALUE>
ALLOWED_HOSTS=<>
```

Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте корректность установки Docker-compose:
```
sudo  docker-compose --version
```

### После успешного деплоя:
На сервере соберите docker-compose:
```
sudo docker compose -f docker-compose.production.yml up -d
```
Проверьте, запустились ли контейнеры
```
sudo docker compose -f docker-compose.production.yml ps
```
Соберите статические файлы и скопируйте их в /backend_static/static/:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static
```
Примените миграции:
```
(опционально) sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
```
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
Создайте суперпользователя:
```
sudo docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```
Зайдите в админку, импортируйте ингредиенты из папки Data и создайте хотя бы 3 тега:


### Развёрнутый проект:

https://myrecipes.sytes.net

## Об авторе
[Боярчук Василий](https://github.com/Milkyaway13/)
