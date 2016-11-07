# Django-Redis-API-


API for TVF media with Redis and Django

- Install the dependencies

sudo pip install requirement.txt

import the data to redis from json file:

Used the below script to load the data to redis:

import json
import redis
import os,sys
datum= []
port=22919, db=1)
r = redis.StrictRedis(host='localhost', port=6379, db=1)
with open('interview.json') as data_file:
    test_data = json.load(data_file)
r.set('tvf_json', test_data)


Once the import is done:

- Start the Djjango App service by running this Command

python manage.py runServer --optional --PORT

by default it will run it in the 127.0.0.1:8000

so based on the each API end point i've postprocessed the data and rendering it as a json


now we can access the and points and get the result as JsonResponse


For Postman : simply pass the below urls with GET Method

https://kovalan-tvfapi.herokuapp.com/tvf/ratingsort?sort=desc

https://kovalan-tvfapi.herokuapp.com/tvf/ratingsort?sort=asc

https://kovalan-tvfapi.herokuapp.com/tvf/list?type=video

https://kovalan-tvfapi.herokuapp.com/tvf/list?type=story

https://kovalan-tvfapi.herokuapp.com/tvf/categories

https://kovalan-tvfapi.herokuapp.com/tvf/all