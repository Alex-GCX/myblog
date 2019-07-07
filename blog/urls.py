from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name ='index'),
    path('detail/<int:article_id>/',views.detail, name ='detail'),
    path('edit/<int:article_id>/',views.edit,name = 'edit'),
]