# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


# ── REGISTER ──────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name',  '').strip()
        username   = request.POST.get('username',   '').strip()
        email      = request.POST.get('email',      '').strip()
        password   = request.POST.get('password',   '')
        password2  = request.POST.get('password_confirm', '')
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'accounts/register.html')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'accounts/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return render(request, 'accounts/register.html')
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'accounts/register.html')
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
        )
        # Create empty profile automatically
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name or user.username}!')
        return redirect('home')
    return render(request, 'accounts/register.html')


# ── LOGIN ─────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'accounts/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '')
            return redirect(next_url if next_url else 'home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


# ── LOGOUT ────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('home')


# ── DASHBOARD ─────────────────────────────────────────
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    from jobs.models import Job
    recent_jobs = Job.objects.order_by('-id')[:6]
    total_jobs  = Job.objects.count()
    profile, _  = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/dashboard.html', {
        'user':        request.user,
        'profile':     profile,
        'recent_jobs': recent_jobs,
        'total_jobs':  total_jobs,
    })


# ── PROFILE EDIT ──────────────────────────────────────
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Personal Info
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name  = request.POST.get('last_name',  '').strip()
        request.user.email      = request.POST.get('email',      '').strip()
        request.user.save()

        profile.mobile           = request.POST.get('mobile',           '').strip()
        profile.location         = request.POST.get('location',         '').strip()
        profile.bio              = request.POST.get('bio',              '').strip()

        # Qualification
        profile.qualification    = request.POST.get('qualification',    '').strip()
        profile.university       = request.POST.get('university',       '').strip()
        profile.graduation_year  = request.POST.get('graduation_year',  '').strip()

        # Job Preferences
        profile.preferred_job_type = request.POST.get('preferred_job_type', '').strip()
        profile.preferred_skills   = request.POST.get('preferred_skills',   '').strip()
        profile.preferred_location = request.POST.get('preferred_location', '').strip()
        profile.expected_salary    = request.POST.get('expected_salary',    '').strip()

        # Last Company
        profile.last_company     = request.POST.get('last_company',     '').strip()
        profile.last_job_title   = request.POST.get('last_job_title',   '').strip()
        profile.last_job_from    = request.POST.get('last_job_from',    '').strip()
        profile.last_job_to      = request.POST.get('last_job_to',      '').strip()
        profile.experience_years = request.POST.get('experience_years', '').strip()
        profile.last_job_desc    = request.POST.get('last_job_desc',    '').strip()

        # Resume upload
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')

    return render(request, 'accounts/profile.html', {
        'user':    request.user,
        'profile': profile,
    })