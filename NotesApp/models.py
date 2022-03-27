from django.db import models
from django.contrib.auth.models import User

# Category : Study Material or Interview Prep => Categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Note(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default='other')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, default='other')
    file = models.FileField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    isApproved = models.BooleanField(default=False)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)