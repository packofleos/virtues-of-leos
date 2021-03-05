from django.urls import path

from . import views

app_name = 'virtues'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('titles/', views.show_titles, name='titles')
]