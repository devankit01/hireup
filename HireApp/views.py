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
    work_list = []
    for work in works:
        work_dict = {}
        work_dict['work_name'] = work.work_name
        work_dict['Type'] = work.Type
        work_dict['emp_type'] = work.emp_type
        work_dict['company'] = work.company
        work_dict['experience_or_time'] = work.experience_or_time
        work_dict['location'] = work.location
        work_dict['salary_or_stipend'] = work.salary_or_stipend
        work_dict['tech_stack'] = eval(work.tech_stack)
        work_dict['number_of_vacancy'] = work.number_of_vacancy
        work_dict['status'] = work.status
        work_dict['applicants'] = work.applicants
        work_dict['resume_selected'] = work.resume_selected
        work_dict['hired'] = work.hired
        work_list.append(work_dict)
    data = {'data': work_list}
    return render(request, 'admin-ui/hireUp/Admin.html', data)
