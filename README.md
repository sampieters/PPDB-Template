# PPDB-Template
Step-by-Step tutorial for a Python database-backed web application with relational database. By Sam Pieters assistant at the University of Antwerp (Belgium) within the Adrem data lab research group.

## Features
This is a Flask-based API website that integrates with a PostgreSQL database using SQLAlchemy. The application supports Server-Side Rendering (SSR) with multiple frontend frameworks, including HTML, React, Vue.

### Relational Database: PostgreSQL

### RESTful API with Flask

### Database ORM with SQLAlchemy

### PostgreSQL integration with SQLAlchemy

### SSR options with HTML, React, Vue, and AJAX

## Quick Start

### Creating the database

**1) Install dependencies** 
```bash
sudo apt install postgresql
```
**2) Create the database** 

First configure the database with ``postgres`` user:
```bash
sudo su postgres
```

Connect to postgres
```bash
psql
```

Then create a role 'librarian' that will create the database and be used by the application:
```postgres
CREATE ROLE librarian WITH LOGIN CREATEDB;
CREATE DATABASE library OWNER librarian;
```
You need to 'trust' the role to be able to login. Add the following line to /etc/postgresql/\<version\>/main/pg_hba.conf (you need root access, version may vary (e.g. 9.6)). **It needs to be the first rule (above local all peer).**
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

local   library         librarian                               trust
```
and restart the service. Then initialize the database:
```bash
sudo systemctl restart postgresql
```

### Run the API locally
**1) Download the project** 
```
git clone https://github.com/sampieters/PPDB-Template.git
```
**2) Create a virtual environment and install the necessary packages** 

```bash
cd PPDB-Template
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3) Run the development server** 
```bash
cd src
python3 app.py
```
Then visit http://localhost:5000

**4) Result**

(TODO)

### Create GCP instance

**1) Access a GCP project and give every team member access**

Provide a ``@gmail.com`` email address via the assignment on Blackboard. This account will be added to a GCP project that you can find via the console: https://console.cloud.google.com/.

Before continuing, add your team members to this project as well through the ``IAM & Admin > IAM`` menu.

**2) Create a Compute instance (VM)**


### Run the API on the GCP instance
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
sudo ln -s /home/app/PPDB-Template-App/service/webapp.service /etc/systemd/system/

sudo systemctl enable webapp
sudo systemctl start webapp
```

A file ``src/ProgDBTutor/webapp.sock`` should be created.

**6) Setup nginx**

Link or copy the nginx server block configuration file to the right nginx folders:

```bash
sudo ln -s /home/app/PPDB-Template-App/nginx/webapp /etc/nginx/sites-available/
sudo ln -s /home/app/PPDB-Template-App/nginx/webapp /etc/nginx/sites-enabled/
```

The contents of this file can be changed for your setup. For example change the IP address to your external IP and add the correct DNS name (``team[x].ua-ppdb.me``)

```json
server {
    listen 80;
    server_name 0.0.0.0 team[x].ua-ppdb.me;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/app/PPDB-Template-App/src/ProgDBTutor/webapp.sock;
    }
}
```

Test the configuration with ``sudo nginx -t``.

**7) Restart the server**

Restart the server with ``sudo systemctl restart nginx``. Your application should be available on port 80.