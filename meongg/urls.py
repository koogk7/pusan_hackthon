from django.urls import path, include

from meongg import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update, name='update'),
    path('add/value', views.addValue, name='add'),
]