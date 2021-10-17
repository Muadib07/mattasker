from django.urls import path

from . import views

app_name = 'task_view'

urlpatterns = [
    # path('hello/', views.hello, name='hello_user'),
    path('', views.tasks_list, name='task_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:task>/', views.task_detail, name='task_detail'),
]