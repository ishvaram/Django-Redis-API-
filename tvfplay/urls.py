import sys,os
file_path = os.path.dirname(__file__).rsplit('/', 1)[0]
sys.path.append(file_path + '/tvfplay/views')
from django.conf.urls import url
from . import views
from tvfredis import index, category, all_items, listbytype, ratingsort

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^categories$', category),
    url(r'^all$', all_items),
    url(r'^list$', listbytype),
    url(r'^ratingsort$', ratingsort)
]

