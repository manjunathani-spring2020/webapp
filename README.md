# Account and Bill management App

## Overview
**myaccountapp** is a Django project containing various apis for user accounts and bills

## Requirements to run the application:
* Django 2.0+
* Uses pip - the officially recommended Python packaging tool from Python.org.
* MySQL database support with mysqlclient.
* The application uses django and mysql, so to test the application locally both django and mysql should be configured. 
  If you are using MYSQL version > 5.* , then you ned to configure the root password authentication to be able to make it work with django.
```
 ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'yourrootpass';
```
* Install the below dependencies.

```
% sudo pip install django==3.0.2
% sudo pip install djangorestframework
% sudo pip install mysqlclient
% sudo pip install django_mysql
% sudo pip install bcrypt==3.1.7
```
**[Django Extensions](https://github.com/django-extensions/django-extensions)** is used for various useful django commands.

## How to run the application
* Navigate to
```
cd myaccountapp
```
* Instructions to run migrations when we make changes to the models.
```
python manage.py makemigrations
python manage.py migrate
```
* Instructions to run the application
```
python manage.py runserver
```

## Unit Tests
* To run our unit test.
```
python manage.py test
```

## Git Instructions
* Create your own fork or clone
  https://github.com/manjunathani-spring2020/webapp