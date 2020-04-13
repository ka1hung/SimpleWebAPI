# SimpleWebAPI

simple web api example present by flask with python3

## Feature

1. allow cors
2. JSON data Formate

## Quick start

### 1.install flask

    pip install flask
    pip install flask-cors

### 2.start

    python main.py

### 3.test

    link to http://127.0.0.1:8000

## API list

### Get all tags

    GET http://127.0.0.1:8000/tags

### write single tag

    GET http://127.0.0.1:8000/writetag?n=TD1&v=0

### read multy Tags

    POST http://127.0.0.1:8000/readtags

    Body: 
            ["TA1","TA2","rr"]

### write multy Tags

    POST 127.0.0.1:8000/writetags
    
    Body:
            [
                {
                    "Name": "TA1",
                    "Value": 123
                },
                {
                    "Name": "TA2",
                    "Value": 2
                }
            ]

## Postman export file

    https://github.com/ka1hung/SimpleWebAPI/blob/master/SimpleWebAPI.postman_collection.json
