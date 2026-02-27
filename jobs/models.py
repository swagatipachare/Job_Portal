from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Job(models.Model):

    JOB_TYPES = (
        ('intern', 'Internship'),
        ('fresher', 'Fresher'),
        ('fulltime', 'Full Time'),
    )

    SKILLS = (
        ('python', 'Python'),
        ('php', 'PHP'),
        ('java', 'Java'),
        ('wordpress', 'WordPress'),
        ('ml', 'Machine Learning'),
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.IntegerField()

    description = models.TextField(default="No description provided")
    requirements = models.TextField(default="No requirements specified")

    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    skill = models.CharField(max_length=50, choices=SKILLS)

    apply_link = models.URLField(default="https://example.com")

    def salary_lpa(self):
        return round((self.salary * 12) / 100000, 1)

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} → {self.job}"