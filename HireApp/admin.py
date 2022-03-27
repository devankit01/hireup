from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(CompanyProfile)
admin.site.register(Work)
admin.site.register(UserProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Skill)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(Experience)