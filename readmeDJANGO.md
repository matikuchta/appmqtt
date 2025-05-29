# DJANGO REST API
## launching the API
### enter the personapi folder inside the server directory
```
cd .\server\personsapi\
```
### launch the server
use this command inside the ```server/personsapi``` directory
```
daphne personsapi.asgi:application
```
the api will launch on port 8000
## example html site using the api 
```/client/index.html```
you have to create an account using the GUI on the site in order to see the database

to manage user accounts you have to create a superuser
```
python manage.py createsuperuser
```
then open ```<serveradress>/api/admin```
default server adress is 127.0.0.1:8000
you can configure this in ```index_dj.js``` in the first fer lines, eg.
``` JS
let config = {
  server: "http://192.168.8.129",
  port: "5140",
};
```


if your server cannot find some js or css files, use 
```
python manage.py collectstatic
```