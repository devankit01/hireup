from unittest import expectedFailure
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import datetime


class UserProfile(models.Model):
    fb = models.CharField(max_length=100)
    lkd = models.CharField(max_length=100)
    git = models.CharField(max_length=100)
    hacker = models.CharField(max_length=100)
    bio = models.TextField(max_length=200)
    phone = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(max_length=210, null=True)
    portfolio = models.CharField(max_length=210, null=True)
    profile = models.CharField(max_length=210, null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=30, null=True)
    emoji = models.CharField(max_length=30, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username)


class Certification(models.Model):
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=10)
    issue_date = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username)


class Experience(models.Model):
    organisation = models.CharField(max_length=100, null=True)
    start_year = models.CharField(max_length=20, null=True)
    end_year = models.CharField(max_length=20, null=True)
    designation = models.CharField(max_length=100, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Education(models.Model):
    name = models.CharField(max_length=100, null=True)
    start_year = models.CharField(max_length=100, null=True)
    end_year = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=20, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username)


# Create your models here.
class CompanyProfile(models.Model):
    ''' Model for Company Profile '''
    company_name = models.CharField(max_length=255, null=True)
    company_type = models.CharField(max_length=30, null=True)
    company_specialization = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=20, null=True)
    company_logo = models.ImageField(upload_to="company_logo", null=True)
    about_company = models.TextField(null=True)
    company_site = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)


class RecruiterProfile(models.Model):
    company = models.ForeignKey(
        CompanyProfile, on_delete=models.DO_NOTHING,  null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)


class Work(models.Model):
    TYPE = (('INTERNSHIP', 'INTERNSHIP'), ('JOB', 'JOB'))
    EMP = (('Part Time Job', 'Part Time Job'),
           ('Full Time Job', 'Full Time Job'))
    Type = models.CharField(max_length=20)
    emp_type = models.CharField(max_length=50)
    work_name = models.CharField(max_length=100)
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE)
    experience_or_time = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    salary_or_stipend = models.CharField(max_length=20)

    about = RichTextField()
    min_requirement = RichTextField()
    tech_stack = models.CharField(max_length=100)
    posted = models.DateTimeField(auto_now_add=True)
    number_of_vacancy = models.CharField(max_length=3)
    status = models.BooleanField(default=True)
    applicants = models.ManyToManyField(UserProfile)
    resume_selected = models.ManyToManyField(
        UserProfile, related_name='resume_selected')
    hired = models.ManyToManyField(UserProfile, related_name='hired')
    onboard = models.ManyToManyField(UserProfile, related_name='onboard')
    created_by = models.ForeignKey(
        RecruiterProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.work_name

    def get_date(self):
        time = datetime.now()
        if self.posted.day == time.day:
            try:
                return str(time.hour - self.posted.hour) + " hours ago"
            except Exception as e:
                print(e)
                return "0 hours ago"
        else:
            if self.posted.month == time.month:
                return str(time.day - self.posted.day) + " days ago"
            else:
                if self.posted.year == time.year:
                    return str(time.month - self.posted.month) + " months ago"
        return self.posted


class Round(models.Model):
    name = models.CharField(max_length=255, null=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    selected = models.ManyToManyField(UserProfile, related_name='selected')

    def __str__(self):
        return self.name
