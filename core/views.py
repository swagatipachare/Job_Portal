from django.shortcuts import render
from jobs.models import Job

from django.shortcuts import render
from jobs.models import Job

def home(request):

    jobs = Job.objects.all()

    job_type = request.GET.get('job_type')
    skill = request.GET.get('skill')

    if job_type and skill:
        jobs = jobs.filter(job_type=job_type, skill=skill)

    elif job_type:
        jobs = jobs.filter(job_type=job_type)

    elif skill:
        jobs = jobs.filter(skill=skill)

    return render(request, 'core/home.html', {'jobs': jobs})