# bucketlist-api

[![Build Status](https://travis-ci.org/inno-asiimwe/bucketlist-api.svg?branch=development)](https://travis-ci.org/inno-asiimwe/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/inno-asiimwe/bucketlist-api/badge.svg?branch=development)](https://coveralls.io/github/inno-asiimwe/bucketlist-api?branch=development)
[![Code Climate](https://codeclimate.com/github/inno-asiimwe/bucketlist-api/badges/gpa.svg)](https://codeclimate.com/github/inno-asiimwe/bucketlist-api)

## Technologies used 
1. Python
2. Flask
3. Postgresql
4. Nosetest
5. Swagger

## How to install
1. Clone repository
2. Install dependencies
   ``` pip install -r requirements.txt ```
3. create database
    ``` manage.py db init ```
    ``` manage.py db migrate ```
    ``` manage.py db upgrade ```
3. Run application using 
   ``` python run.py ```

## Features implemented
* User registration
* User login and logout
* Bucketlist creation, editing and deletion
* Bucketlist item creation, editing and deletion
* Search by bucketlist by name
* pagination of results

## Running Tests
   ``` nosetests ```

## Documentation 

Documentation for the api can be found at the following urls:
``` http://127.0.0.1:5000/apidocs/ ```


