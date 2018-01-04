from django.conf.urls import url
from gastos import models, views


# Add a new patern for each normal class in models file
urlpatterns = [
    url(r'^filter/by_concept/(?P<pattern>.+)$', views.filter_by_concept, name='filter_by_concept'),
    url(r'^add_tags/(?P<ct>\d+)/(?P<ids>.+)$', views.add_tags, name='add_tags'),
    url(r'^list_tags$', views.list_tags, name='list_tags')
]
