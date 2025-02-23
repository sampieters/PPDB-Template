# Run the API on the GCP instance
These steps demonstrate how to run this application with nginx. They are to be executed in addition to the setup in quick start. Instead of running the built in Flask debug server, we use an industrial grade webserver and reverse proxy server: nginx.

**1) Install dependencies**
```bash
sudo apt install nginx
```
**2) Create user to run application**
```bash
sudo adduser --disabled-login app
sudo su - app
```
When asked for settings (Full Name, Room Number, ...) just press enter on all values. Then press ``y`` for Yes.

(optional): If running sudo ``sudo su - app`` gives the error **"This account is currently not available."**, you need to fix the app user's settings and try again:
```bash
sudo usermod -s /bin/bash app
sudo su - app
```

**3) Follow Quick start to setup the project**

Check Quick Start

**4) Test if wsgi entrypoint works**

Instead of using the Flask debug server, we use gunicorn to serve the application.

```bash
cd src
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

**5) Enable the webservice**

As an account with sudo acces (not app), copy the file ``service/webapp.service`` to ``/etc/systemd/system/`` and enable the service:

```bash
sudo ln -s /home/app/PPDB-Template/service/webapp.service /etc/systemd/system/

sudo systemctl enable webapp
sudo systemctl start webapp
```

A file ``src/webapp.sock`` should be created.

**6) Setup nginx**

Link or copy the nginx server block configuration file to the right nginx folders:

```bash
sudo ln -s /home/app/PPDB-Template/nginx/webapp /etc/nginx/sites-available/
sudo ln -s /home/app/PPDB-Template/nginx/webapp /etc/nginx/sites-enabled/
```

The contents of this file can be changed for your setup. For example change the IP address to your external IP and add the correct DNS name (``team[x].ua-ppdb.me``)

```
server {
    listen 80;
    server_name 0.0.0.0 team[x].ua-ppdb.me;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/app/PPDB-Template/src/webapp.sock;
    }
}
```

Test the configuration with ``sudo nginx -t``.

**7) Restart the server**

Restart the server with ``sudo systemctl restart nginx``. Your application should be available on port 80.