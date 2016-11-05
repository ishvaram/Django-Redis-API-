import os, sys, string, json, ast
import re
import math
import datetime
import urllib
import collections
from django.db import connections
from django.http import HttpResponse,JsonResponse
from django.core.serializers.json import json, DjangoJSONEncoder
from common_views import *
import redis
import unicodedata


redis_con = redis.StrictRedis(host='localhost', port=6379, db=1)

def index(request):
  	return ("Welcome to Redis TVF API")


def all_items(request):
	'''	List all the the Dict from Redis
	'''
	try:
		if redis_con:
			datum = redis_con.get('tvf_json')
			datum = ast.literal_eval(datum)
			return HttpResponse(json.dumps(datum, cls=DjangoJSONEncoder), content_type='application/json', status=200)
		else:
			return HttpResponse("Not able to connect To Redis", status=200)

	except Exception, e:
		response = {'status':'Request Failure','message':e}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=500)


def category(request):
	'''	List all the Categories
	'''
	categories = {'categories': []}
	try:
		if redis_con:
			datum = redis_con.get('tvf_json')
			datum = ast.literal_eval(datum)
			for x in datum:
				categories['categories'].append(x['category_name'])
			return HttpResponse(json.dumps(categories, cls=DjangoJSONEncoder), content_type='application/json', status=200)
		else:
			return HttpResponse("Not able to connect To Redis", status=200)

	except Exception, e:
		response = {'status':'Request Failure','message':e}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=500)

def listbytype(request):
	''' List all the items by type
	'''
	sortbytype = {'result':[]}
	try:
		datum = redis_con.get('tvf_json')
		datum = ast.literal_eval(datum)
		if 'type' not in request.GET:
			response = {'status':'Request Failure','message':'Incorrect request. The Type param is missing/invalid in the request'}
			return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=403)
		else:
			if request.GET['type'] == '':
				response = {'status':'Request Failure','message':'Incorrect request. The Type param is missing/invalid in the request'}
				return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=403)
		for x in datum:
			if request.GET['type'] == 'story':
				if x['type'] == 'story':
					sortbytype['result'].append(x)
			else:
				if x['type'] == 'video':
					sortbytype['result'].append(x)
		return HttpResponse(json.dumps(sortbytype, cls=DjangoJSONEncoder), content_type='application/json', status=200)
	except Exception, e:
		response = {'status':'Request Failure','message':e}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=500)


def ratingsort(request):
	sortbyratings = {'result':[]}
	try:
		datum = redis_con.get('tvf_json')
		datum = ast.literal_eval(datum)
		if 'sort' not in request.GET:
			response = {'status':'Request Failure','message':'Incorrect request. The Sort param is missing/invalid in the request'}
			return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=403)
		else:
			if request.GET['sort'] == '':
				response = {'status':'Request Failure','message':'Incorrect request. The Sort param is missing/invalid in the request'}
				return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=403)

		if request.GET['sort'] == 'asc':
			lines = sorted(datum, key=lambda k: k['rating'], reverse=False)
			sortbyratings['result'].append(lines)
		else:
			lines = sorted(datum, key=lambda k: k['rating'], reverse=True)
			sortbyratings['result'].append(lines)
		return HttpResponse(json.dumps(sortbyratings, cls=DjangoJSONEncoder), content_type='application/json', status=200)
	except Exception, e:
		response = {'status':'Request Failure','message':e}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json', status=500)

				


