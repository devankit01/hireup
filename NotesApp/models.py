from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Category : Study Material or Interview Prep => Categories

# models of study materials


class StudyMaterials(models.Model):
    Years = (
        ("1st", "1st"),
        ("2nd", "2nd"),
        ("3rd", "3rd"),
        ("4th", "4th"),
    )
    Banches = (
        ("CSE", "CSE"),
        ("IT", "IT"),
        ("ME", "ME"),
        ("AG", "AG"),
        ("CE", "CE"),
        ("BT", "BT"),
    )
    subject = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    years = models.CharField(max_length=100, choices=Years)
    Branch = models.CharField(max_length=200, choices=Banches, default=None)
    file = models.FileField(
        upload_to="StudyMaterials/Fileuploads/", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    IsApproved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Name) + str(self.subject)

    def getFile(self):
        domain = 'https://hireup-pdfs.s3.amazonaws.com/'
        url = str(domain) + str(self.file)
        return url


# models of Interview Prep
class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InterviewPrep(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True,
                            upload_to='InterviewPrep/Fileuploads/')
    url = models.URLField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    IsApproved = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

    def getFile(self):
        domain = 'https://hireup-pdfs.s3.amazonaws.com/'
        url = str(domain) + str(self.file)
        return url