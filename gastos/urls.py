from django.conf.urls import url
from gastos import views


# Add a new patern for each normal class in models file
urlpatterns = [
    url(r'^filter/by_concept/(?P<pattern>.+)$',
        views.filter_by_concept, name='filter_by_concept'),
    url(r'^add_tags/(?P<spending_ids>(\d+,?)+)$',
        views.add_tags_view, name='add_tags'),
    url(r'^add_tags_with_regex/(?P<spending_id>\d+)$',
        views.add_tags_with_regex_view, name='add_tags_with_regex'),
    url(r'^list_tags$', views.list_tags_json, name='list_tags')
]
