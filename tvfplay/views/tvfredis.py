'''
!/usr/bin/python
-*- coding: utf-8 -*-
Author: Kovalan R
Date: 05-11-2016
Description: Redis-Django API - its connects to
redis and does the given operations
'''
import sys
import json
import os
import ast
import redis
from django.http import HttpResponse
from django.core.serializers.json import json
from django.core.serializers.json import DjangoJSONEncoder


try:
	REDIS_CONN = redis.from_url(os.environ.get("REDISTOGO_URL"))
except Exception, exc:
	print "Unable to connect to Redis.Please check the redis service is running"
	REDIS_CONN = None


print REDIS_CONN

def insert():
	with open('./interview.json') as data_file:
		test_data = json.load(data_file)
	REDIS_CONN.set('tvf_json', test_data)
	return True


def index():
	''' Index request Funtion
	'''
	return HttpResponse("Welcome to  TVF API Redis-Django")


def all_items():
	'''	List all the the Dict from Redis
	'''
	try:
		if REDIS_CONN:
			datum = REDIS_CONN.get('tvf_json')
			datum = ast.literal_eval(datum)
			return HttpResponse(json.dumps(datum, cls=DjangoJSONEncoder), \
				content_type='application/json', status=200)
		else:
			return HttpResponse("Not able to connect To Redis", status=500)

	except Exception, exc:
		response = {'status': 'Request Failure', 'message': exc}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), \
			content_type='application/json', status=500)


def category():
	'''	List all the Categories
	'''
	categories = {'categories': []}
	try:
		if REDIS_CONN:
			datum = REDIS_CONN.get('tvf_json')
			datum = ast.literal_eval(datum)
			for each in datum:
				categories['categories'].append(each['category_name'])
			return HttpResponse(json.dumps(categories, cls=DjangoJSONEncoder),\
			 content_type='application/json', status=200)
		else:
			return HttpResponse("Not able to connect To Redis", status=500)

	except Exception, exc:
		response = {'status': 'Request Failure', 'message': exc}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),\
		 		content_type='application/json', status=500)


def listbytype(request):
	''' List all the items by type either video or story
	'''
	sortbytype = {'result': []}
	try:
		datum = REDIS_CONN.get('tvf_json')
		datum = ast.literal_eval(datum)
		if 'type' not in request.GET:
			response = {'status': 'Request Failure', \
				'message': 'Incorrect request. The Type param \
				is missing/invalid in the request'}
			return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), \
					content_type='application/json', status=400)
		else:
			if request.GET['type'] == '':
				response = {'status': 'Request Failure', \
					'message': 'Incorrect request. The Type param is \
					missing/invalid in the request'}
				return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),\
				 		content_type='application/json', status=400)
		for each in datum:
			if request.GET['type'] == 'story':
				if each['type'] == 'story':
					sortbytype['result'].append(each)
			else:
				if each['type'] == 'video':
					sortbytype['result'].append(each)
		return HttpResponse(json.dumps(sortbytype, cls=DjangoJSONEncoder), \
		 		content_type='application/json', status=200)
	except Exception, exc:
		response = {'status': 'Request Failure', 'message': exc}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), \
		 		content_type='application/json', status=500)


def ratingsort(request):
	''' Sort the data By ascending and desc
	'''
	sortbyratings = {'result': []}
	try:
		datum = REDIS_CONN.get('tvf_json')
		datum = ast.literal_eval(datum)
		if 'sort' not in request.GET:
			response = {'status': 'Request Failure', \
					'message': 'Incorrect request. The Sort \
					param is missing/invalid in the request'}
			return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), \
					content_type='application/json', status=400)
		else:
			if request.GET['sort'] == '':
				response = {'status': 'Request Failure', \
						'message': 'Incorrect request. The Sort param is \
						missing/invalid in the request'}
				return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),\
					 content_type='application/json', status=400)

		if request.GET['sort'] == 'asc':
			lines = sorted(datum, key=lambda k: k['rating'], reverse=False)
			sortbyratings['result'].append(lines)
		else:
			lines = sorted(datum, key=lambda k: k['rating'], reverse=True)
			sortbyratings['result'].append(lines)
		return HttpResponse(json.dumps(sortbyratings, cls=DjangoJSONEncoder), \
				content_type='application/json', status=200)
	except Exception, exc:
		response = {'status': 'Request Failure', 'message': exc}
		return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), \
				content_type='application/json', status=500)
