from django.shortcuts import render
from .models import Work, CompanyProfile, RecruiterProfile
# Create your views here.


def jobs(request):
    return render(request, 'hireup/jobs.html')


def jobInfo(request, id):
    return render(request, 'hireup/jobInfo.html')


def createJob(request):
    if request.method == 'POST':

        if len(request.POST.getlist('stack')) == 0:
            print("SELECT ATLEAST ONE!")

            return render(request, 'hireup/createjob.html', {'error': 'Please select atleast one technology.'})
        company = RecruiterProfile.objects.filter(
            username=request.user).first()
        print(company)
        job_details = {
            "Type": request.POST['jobType'],
            "emp_type": request.POST['empType'],
            "work_name": request.POST['jobName'],
            "company": company.company,
            "experience_or_time": request.POST['experience'],
            "location": request.POST['location'],
            "salary_or_stipend": request.POST['salary'],
            "tech_stack": request.POST.getlist('stack'),
            "number_of_vacancy": request.POST['opening'],
        }
        print("Creating job........")
        # Work.objects.create(**job_details)

        print("Job Created........")

        return render(request, 'hireup/createjob.html')
    return render(request, 'hireup/createjob.html')


def recruiterJobs(request):
    works = Work.objects.all()
    data = {'data': works}
    return render(request, 'admin-ui/hireUp/Admin.html', data)
