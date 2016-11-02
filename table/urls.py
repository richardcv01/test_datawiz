from django.conf.urls import url

from .import views

app_name = 'table'
urlpatterns = [
    url(r'^$', views.client),
    url(r'^table', views.table, name='table'),

]
