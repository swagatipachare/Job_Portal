# jobs/urls.py
from django.urls import path
from .views import home, job_list, job_detail, apply_job, post_job

urlpatterns = [
    path('',                     home,       name='home'),
    path('jobs/',                job_list,   name='job_list'),
    path('jobs/<int:id>/',       job_detail, name='job_detail'),
    path('jobs/apply/<int:id>/', apply_job,  name='apply_job'),
    path('jobs/post/',           post_job,   name='post_job'),
]