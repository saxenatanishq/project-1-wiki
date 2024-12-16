from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.greet, name='greet'),
    path('search/', views.find , name = "search"),
    path('add/',views.add, name="add"),
    path('new/',views.new,name="new"),
    path('random/',views.randomf,name="random"),
    path('edit/<str:name>',views.edit,name="edit"),
    path('editf/',views.editf,name="editf")
]
