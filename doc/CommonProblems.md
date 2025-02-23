# Common Problems Setting Up The Project



## Creating the database
It is possible that the database can't be accessed by psycopg. To solve this you can change the line in the ``pg_hba.conf`` file to the following:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

host    library         app             127.0.0.1/32            trust
```
and restart the service.
```bash
sudo systemctl restart postgresql
```

## 502 bad gateway
If the website gives the following error 
```
502 bad gateway
```
try to give execute permissions to others for the directory ``/home/app``

```bash
sudo chmod o+x /home/app
```
- **chmod:** Changes file or directory permissions.
- **o+x:** Grants execute (+x) permission to others (anyone who is not the owner or in the group).
- **/home/app:** The target directory whose permissions are being changed.