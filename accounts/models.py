# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Personal Info
    mobile      = models.CharField(max_length=15,  blank=True)
    location    = models.CharField(max_length=100, blank=True)

    # Resume & Qualifications
    resume      = models.FileField(upload_to='resumes/',       blank=True, null=True)
    qualification = models.CharField(max_length=200,           blank=True,
                    help_text="e.g. B.Tech Computer Science, MBA")
    university  = models.CharField(max_length=200,             blank=True)
    graduation_year = models.CharField(max_length=4,           blank=True)

    # Job Preferences
    JOB_TYPE_CHOICES = [
        ('fulltime', 'Full Time'),
        ('intern',   'Internship'),
        ('fresher',  'Fresher'),
        ('remote',   'Remote'),
        ('hybrid',   'Hybrid'),
    ]
    preferred_job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, blank=True)
    preferred_skills   = models.CharField(max_length=300, blank=True,
                         help_text="e.g. Python, React, Django")
    preferred_location = models.CharField(max_length=100, blank=True)
    expected_salary    = models.CharField(max_length=50,  blank=True,
                         help_text="e.g. 8-12 LPA")

    # Last Company / Work Experience
    last_company    = models.CharField(max_length=200, blank=True)
    last_job_title  = models.CharField(max_length=200, blank=True)
    last_job_from   = models.CharField(max_length=20,  blank=True, help_text="e.g. Jan 2022")
    last_job_to     = models.CharField(max_length=20,  blank=True, help_text="e.g. Dec 2023 or Present")
    experience_years= models.CharField(max_length=10,  blank=True, help_text="e.g. 2.5")
    last_job_desc   = models.TextField(blank=True,     help_text="Brief description of responsibilities")

    # Bio
    bio             = models.TextField(blank=True, max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def resume_filename(self):
        if self.resume:
            return self.resume.name.split('/')[-1]
        return None

    @property
    def profile_completion(self):
        """Returns % of profile completed."""
        fields = [
            self.mobile, self.location, self.resume,
            self.qualification, self.preferred_job_type,
            self.preferred_skills, self.last_company,
            self.experience_years, self.bio,
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)