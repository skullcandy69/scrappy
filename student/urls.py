from django.urls import path, include
from . import views

urlpatterns = [
    path('function', views.function,name='function'),
    path('add', views.add,name='add'),
    path('func', views.func,name='func'),
    path('', views.home,name='home'),
]
