from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives
from HireApp.models import RecruiterProfile, Skill, UserProfile
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import F, Q
from HireApp.models import CompanyProfile
from HireApp.models import Work, Education, Experience, Certification
from datetime import datetime
from django.http import FileResponse


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


# Create your views here.
def index(request):
    jobs = Work.objects.filter(status=True)
    return render(request, 'index.html', {'jobs': jobs})


def Usersignup(request):
    User = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if User.objects.filter(email=email).count() == 0:
            email = request.POST.get('email')
            user = User(username=email, email=email,
                        password=request.POST.get('password'))
            user.is_active = False
            user.save()
            UserProfile.objects.create(username=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Seeker account.'
            message = render_to_string('email/email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            # send_mail(mail_subject, message, 'youremail', [to_email])
            msg = EmailMultiAlternatives(
                mail_subject, message, 'youremail', [to_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            return render(request, 'users/userSignup.html', {"data": 'Please confirm your email address to complete the registration'})
        else:
            return render(request, 'users/userSignup.html', {"data": 'User Already Registered'})

    return render(request, 'users/userSignup.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def Recruitersignup(request):

    if request.method == 'POST':
        User = get_user_model()
        email = request.POST.get('email', None)
        if User.objects.filter(email=email).count() == 0:
            email = request.POST.get('email')
            user = User(username=email, email=email,
                        password=request.POST.get('password'))
            user.is_active = False
            user.save()
            RecruiterProfile.objects.create(username=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Recruiter account.'
            message = render_to_string('email/email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            # send_mail(mail_subject, message, 'youremail', [to_email])
            msg = EmailMultiAlternatives(
                mail_subject, message, 'youremail', [to_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            return render(request, 'users/recruiterSignup.html', {"data": 'Please confirm your email address to complete the registration'})
        else:
            return render(request, 'users/recruiterSignup.html', {"data": 'User Already Registered'})

    return render(request, 'users/recruiterSignup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(username=email).first()
            if user.password == password:
                status = True
            else:
                status = False
            if status and user.is_active:

                auth.login(request, user)
                request.session['username'] = email
                return redirect('userprofile')
            else:
                return render(request, 'users/signin.html', {'data': 'Invalid Credentials'})

        except Exception as e:
            return redirect('signin')
    return render(request, 'users/signin.html')


def userprofile(request):
    try:
        if request.session.get('username', None):
            user = get_object_or_404(User, username=request.user)
            user_profile = UserProfile.objects.filter(username=user)
            if user_profile.exists():
                user_profile = user_profile.first()
                if not user.first_name:
                    print('Have to add profile first!')
                    user_profile.page = 'Edit'
                    user_profile.button = 'Update'
                    return render(request, 'users/editUserProfile.html', {"data": user_profile})
                user_profile.first_name = user.first_name
                user_profile.last_name = user.last_name
                skill_object = Skill.objects.filter(
                    username=request.user)
                if skill_object.exists():
                    user_profile.tech_stack = eval(skill_object.first().name)
                # EDUCATION
                user_profile.education = Education.objects.filter(
                    username=request.user).order_by('start_year')
                # EDUCATION

                # EXPERIENCE
                user_profile.experience = Experience.objects.filter(
                    username=request.user).order_by('start_year')
                # EXPERIENCE

                # CERTIFICATION
                user_profile.certification = Certification.objects.filter(
                    username=request.user).order_by('issue_date')
                # CERTIFICATION

                return render(request, 'users/userProfile.html', {"data": user_profile})

            if RecruiterProfile.objects.filter(username=user).exists():
                print('Recruiter')
                companyDetail = RecruiterProfile.objects.filter(
                    username=user).values(comp_id=F('company__id'), company_name=F('company__company_name'), company_type=F('company__company_type'), company_specialization=F('company__company_specialization'), company_phone=F('company__phone'), company_logo=F('company__company_logo'), about_company=F('company__about_company'), company_site=F('company__company_site'), company_location=F('company__location'), user_phone=F('phone')).first()
                companyDetail['first_name'] = user.first_name
                companyDetail['last_name'] = user.last_name
                if companyDetail['company_name'] != '' and companyDetail['company_name'] != None:
                    companyDetail['company'] = False
                else:
                    companyDetail['company_list'] = CompanyProfile.objects.all()
                    companyDetail['company'] = True
                if user.first_name:
                    return render(request, 'users/recruiterProfile.html', companyDetail)
                else:
                    return redirect('editRecruiterProfile')
        else:
            return render(request, 'users/recruiterProfile.html')

    except Exception as e:
        print(e)
        return render(request, 'users/signin.html')


def logout(request):

    uid = User.objects.get(username=request.user)
    auth.logout(request)

    if request.session.has_key('username'):
        del request.session['username']
    else:
        pass

    return redirect('signin')


def editCompany(request, id=None):
    if request.method == 'POST':
        company_details = {
            "company_name": request.POST['company_name'],
            "company_type": request.POST['company_type'],
            "company_specialization": request.POST['company_specialization'],
            "phone": request.POST['phone'],
            "location": request.POST['location'],
            "about_company": request.POST['about_company'],
            "company_site": request.POST['company_site'],
        }

        if request.FILES.get('company_logo', None):
            company_details['company_logo'] = request.FILES['company_logo']
        if id:  # will update existing company details
            company = CompanyProfile(id=id)
            company.company_name = company_details['company_name']
            company.company_type = company_details['company_type']
            company.company_specialization = company_details['company_specialization']
            company.phone = company_details['phone']
            company.about_company = company_details['about_company']
            company.company_site = company_details['company_site']
            company.location = company_details['location']
            if request.FILES.get('company_logo', None) == None:
                company.company_logo = CompanyProfile.objects.filter(
                    id=id).first().company_logo
            else:
                company.company_logo = company_details['company_logo']
            company.save()
        else:  # will create new company
            company = CompanyProfile.objects.create(**company_details)
            RecruiterProfile.objects.filter(
                username=request.user).update(company=company)
        return redirect('userprofile')
    if id == None:
        return render(request, 'users/editCompany.html', {'button': 'Save', 'page': 'Add'})
    else:
        companyProfile = CompanyProfile.objects.filter(id=id).first()
        return render(request, 'users/editCompany.html', {'data': companyProfile, 'button': 'Update', 'page': 'Edit'})


def setCompany(request):
    if request.method == 'POST':
        name = request.POST.get('company')
        if name != '' and name != None:
            company = CompanyProfile.objects.filter(company_name=name).first()
            RecruiterProfile.objects.update(company=company)
            return redirect('userprofile')
        return redirect('userprofile')


def editRecruiterProfile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user)
        if RecruiterProfile.objects.filter(username=user).count():
            print('Recruiter')
            RecruiterProfile.objects.filter(
                username=request.user).update(phone=request.POST['phone'])
            user_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email']
            }
            User.objects.filter(username=request.user).update(**user_data)

            companyDetail = RecruiterProfile.objects.filter(
                username=user).values(comp_id=F('company__id'), company_name=F('company__company_name'), company_type=F('company__company_type'), company_specialization=F('company__company_specialization'), company_phone=F('company__phone'), company_logo=F('company__company_logo'), about_company=F('company__about_company'), company_site=F('company__company_site'), company_location=F('company__location'), user_phone=F('phone')).first()
            companyDetail['first_name'] = request.POST['first_name']
            companyDetail['last_name'] = request.POST['last_name']
            if companyDetail['company_name'] != '' and companyDetail['company_name'] != None:
                companyDetail['company'] = False
                companyDetail['company_list'] = CompanyProfile.objects.all()
            else:
                companyDetail['company'] = True
            companyDetail['page'] = 'Edit'
            companyDetail['button'] = 'Update'
            return render(request, 'users/recruiterProfile.html', companyDetail)
    user_data = User.objects.filter(username=request.user).first()
    data = {
        'phone': RecruiterProfile.objects.filter(username=request.user).first().phone,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'email': user_data.email,
        'page': 'Add',
        "button": "Save"
    }

    return render(request, 'users/editRecruiterProfile.html', data)


def editUserProfile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user)
        user_profile = UserProfile.objects.filter(username=user)
        if user_profile.exists():
            user_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email']
            }
            User.objects.filter(username=request.user).update(**user_data)

            user_resume_update = UserProfile(id=user_profile.first().id)

            user_resume_update.phone = user_data['phone'] = request.POST.get(
                'phone', None)
            user_resume_update.fb = user_data['fb'] = request.POST.get(
                'fb', None)
            user_resume_update.lkd = user_data['lkd'] = request.POST.get(
                'lkd', None)
            user_resume_update.git = user_data['git'] = request.POST.get(
                'git', None)
            user_resume_update.hacker = user_data['hacker'] = request.POST.get(
                'hacker', None)
            user_resume_update.bio = user_data['bio'] = request.POST.get(
                'bio', None)
            user_resume_update.profile = user_data['profile'] = request.POST.get(
                'profile', None)
            user_resume_update.username = user
            if request.FILES.get('resume', None):
                user_resume_update.resume = request.FILES['resume']
            else:
                user_resume_update.resume = user_resume_update.resume
                user_data['resume'] = user_resume_update.resume
            user_resume_update.save()

            # adding skills
            skill_objects = Skill.objects.filter(username=request.user)
            if skill_objects.exists():
                skill_objects.update(
                    name=request.POST.getlist('stack'))
            else:
                Skill.objects.create(username=request.user,
                                     name=request.POST.getlist('stack'))

            user_data['tech_stack'] = request.POST.getlist('stack')
            return render(request, 'users/userProfile.html', {"data": user_data})
    user_data = User.objects.filter(username=request.user).first()
    user_basic_info = UserProfile.objects.filter(username=request.user).first()
    skills = Skill.objects.filter(username=request.user).first()
    data = {
        'phone': user_basic_info.phone,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'email': user_data,
        'fb': user_basic_info.fb,
        'lkd': user_basic_info.lkd,
        'git': user_basic_info.git,
        'hacker': user_basic_info.hacker,
        'bio': user_basic_info.bio,
        'profile': user_basic_info.profile,
        'page': 'Add',
        "button": "Save"
    }
    if skills:
        data['tech_stack'] = eval(skills.name)
    return render(request, 'users/editUserProfile.html', {"data": data})


def addEdu(request, id=None):
    if request.method == 'POST':
        if id:
            education_object = Education(id=id)
            print('-----------education_object-------------------')
        else:
            education_object = Education()
        education_object.name = request.POST['name']
        start_year = request.POST['start_year']
        start_year = datetime.strptime(start_year, '%Y-%m-%d')
        start_year = datetime.strftime(start_year, '%B %Y')
        education_object.start_year = start_year

        end_year = request.POST['end_year']
        end_year = datetime.strptime(end_year, '%Y-%m-%d')
        end_year = datetime.strftime(end_year, '%B %Y')
        education_object.end_year = end_year
        education_object.degree = request.POST['degree']
        education_object.username = request.user
        education_object.save()
        return redirect('userprofile')
    if id:
        data = Education.objects.filter(username=request.user).first()
        return render(request, 'hireup/AddEditEdu.html', {"data": data})

    return render(request, 'hireup/AddEditEdu.html')


def addExp(request, id=None):
    if request.method == 'POST':
        if id:
            experience_object = Experience(id=id)
        else:
            experience_object = Experience()
        experience_object.organisation = request.POST['organisation']

        start_year = request.POST['start_year']
        start_year = datetime.strptime(start_year, '%Y-%m-%d')
        start_year = datetime.strftime(start_year, '%B %Y')
        experience_object.start_year = start_year

        end_year = request.POST['end_year']
        end_year = datetime.strptime(end_year, '%Y-%m-%d')
        end_year = datetime.strftime(end_year, '%B %Y')
        experience_object.end_year = end_year

        experience_object.designation = request.POST['designation']
        experience_object.username = request.user
        experience_object.save()
        return redirect('userprofile')
    if id:
        data = Experience.objects.filter(username=request.user).first()
        return render(request, 'hireup/AddEditExp.html', {"data": data})
    return render(request, 'hireup/AddEditExp.html')


def addCert(request, id=None):
    if request.method == 'POST':
        if id:
            certification_object = Certification(id=id)
        else:
            certification_object = Certification()

        certification_object.name = request.POST['name']
        certification_object.organisation = request.POST['organisation']

        issue_date = request.POST['issue_date']
        issue_date = datetime.strptime(issue_date, '%Y-%m-%d')
        issue_date = datetime.strftime(issue_date, '%B %Y')
        certification_object.issue_date = issue_date

        certification_object.url = request.POST['url']
        certification_object.username = request.user
        certification_object.save()
        return redirect('userprofile')
    if id:
        data = Certification.objects.filter(username=request.user).first()
        return render(request, 'hireup/AddEditCert.html', {"data": data})
    return render(request, 'hireup/AddEditCert.html')


def profile(request, user):
    user = get_object_or_404(User, email=user)
    print(user)
    user_profile = UserProfile.objects.filter(username=user).filter()
    print(user_profile)
    if user_profile.exists():
        user_profile = user_profile.first()

        user_profile.first_name = user.first_name
        user_profile.last_name = user.last_name
        if Skill.objects.filter(
                username=user).exists():
            user_profile.tech_stack = eval(Skill.objects.filter(
                username=user).first().name)
        # EDUCATION
        user_profile.education = Education.objects.filter(
            username=user).order_by('start_year')
        # EDUCATION

        # EXPERIENCE
        user_profile.experience = Experience.objects.filter(
            username=user).order_by('start_year')
        # EXPERIENCE

        # CERTIFICATION
        user_profile.certification = Certification.objects.filter(
            username=user).order_by('issue_date')
        # CERTIFICATION
        user_profile.resume = "https://shift-agreements.s3.ap-south-1.amazonaws.com/" + \
            str(user_profile.resume)

        return render(request, 'users/profile.html', {"data": user_profile, 'user': user})


def resumeViewer(request, user):
    user = get_object_or_404(User, email=user)
    pdf = UserProfile.objects.filter(username=user).first()
    if pdf:
        try:
            print(
                "https://shift-agreements.s3.ap-south-1.amazonaws.com/"+str(pdf.resume))
            return FileResponse(open("https://shift-agreements.s3.ap-south-1.amazonaws.com/"+str(pdf.resume), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404('not found')
