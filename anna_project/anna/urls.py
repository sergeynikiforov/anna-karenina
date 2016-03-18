from django.conf.urls import url

from . import views

app_name = 'anna'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.searchResults, name='results'),
]
