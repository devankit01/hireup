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
from HireApp.models import RecruiterProfile, UserProfile
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import F
from HireApp.models import CompanyProfile
from HireApp.models import Work


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
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return HttpResponse('User Already Registered')

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
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return HttpResponse('User Already Registered')

    return render(request, 'users/recruiterSignup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        try:
            user = User.objects.filter(username=email).first()
            print(user.password, password)
            if user.password == password:
                status = True
            else:
                status = False
            print(status)
            if status and user.is_active:

                auth.login(request, user)
                request.session['username'] = email
                return redirect('userprofile')
            else:
                return HttpResponse('Invalid Credential')

        except Exception as e:
            print(e)
            print('Login Failed')
            return redirect('signin')

    return render(request, 'users/signin.html')


def userprofile(request):
    try:
        if request.session.get('username', None):
            # print(request.session['username'], request.user)
            user = get_object_or_404(User, username=request.user)
            user_profile = UserProfile.objects.filter(username=user)
            if user_profile.exists():
                user_profile = user_profile.first()
                if not user.first_name:
                    print('Have to add profile first!')
                    user_profile.page = 'Add'
                    user_profile.button = 'Save'
                    user_profile.month_names = ['January', 'February', 'March', 'April', 'May',
                                                'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    user_profile.month = ''
                    return render(request, 'users/editUserProfile.html', {"data": user_profile})
                print('User', user_profile)
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
    print(uid)
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
