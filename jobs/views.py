# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job


def home(request):
    job_type = request.GET.get('job_type', '')
    skill    = request.GET.get('skill', '')
    jobs     = Job.objects.all()
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if skill:
        jobs = jobs.filter(skill__iexact=skill)
    skills = Job.objects.values_list('skill', flat=True).distinct().order_by('skill')
    return render(request, 'core/home.html', {'jobs': jobs, 'skills': skills, 'selected_skill': skill, 'selected_type': job_type})


def job_list(request):
    job_type = request.GET.get('job_type', '')
    skill    = request.GET.get('skill', '')
    jobs     = Job.objects.all()
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if skill:
        jobs = jobs.filter(skill__iexact=skill)
    skills = Job.objects.values_list('skill', flat=True).distinct().order_by('skill')
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'skills': skills, 'selected_skill': skill, 'selected_type': job_type})


def job_detail(request, id):
    job          = get_object_or_404(Job, id=id)
    similar_jobs = Job.objects.filter(job_type=job.job_type).exclude(id=id)[:6]
    other_jobs   = Job.objects.exclude(job_type=job.job_type).exclude(id=id)[:6]
    return render(request, 'jobs/job_detail.html', {
        'job':          job,
        'similar_jobs': similar_jobs,
        'other_jobs':   other_jobs,
    })


def apply_job(request, id):
    job = get_object_or_404(Job, id=id)
    if job.apply_link:
        return redirect(job.apply_link)
    return redirect('job_detail', id=id)


@login_required(login_url='login')
def post_job(request):
    # Only staff/admin can post jobs
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to post jobs.')
        return redirect('job_list')
    if request.method == 'POST':
        title        = request.POST.get('title', '').strip()
        company      = request.POST.get('company', '').strip()
        location     = request.POST.get('location', '').strip()
        job_type     = request.POST.get('job_type', '').strip()
        skill        = request.POST.get('skill', '').strip()
        salary       = request.POST.get('salary', 0)
        apply_link   = request.POST.get('apply_link', '').strip()
        description  = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()

        if not title or not company or not location:
            messages.error(request, 'Title, Company and Location are required.')
            return render(request, 'jobs/post_job.html')

        Job.objects.create(
            title        = title,
            company      = company,
            location     = location,
            job_type     = job_type,
            skill        = skill,
            salary       = salary,
            apply_link   = apply_link,
            description  = description,
            requirements = requirements,
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('job_list')

    return render(request, 'jobs/post_job.html')