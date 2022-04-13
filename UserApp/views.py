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


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
            user_authenticate = auth.authenticate(
                username=email, password=password)
            print(user, user_authenticate)
            if user.is_active:
                auth.login(request, user)
                request.session['username'] = email
                getUser = user.email
                print()
                return redirect('userprofile')
        except Exception as e:
            print('Login Failed')
            return redirect('signin')

    return render(request, 'users/signin.html')


def userprofile(request):
    try:
        if request.session.get('username', None):
            # print(request.session['username'], request.user)
            user = get_object_or_404(User, username=request.user)
            if UserProfile.objects.filter(username=user).count():
                print('User')
                return render(request, 'users/userProfile.html')

            if RecruiterProfile.objects.filter(username=user).count():
                print('Recruiter')
                companyDetail = RecruiterProfile.objects.filter(
                    username=user).values(comp_id=F('company__id'), company_name=F('company__company_name'), company_type=F('company__company_type'), company_specialization=F('company__company_specialization'), company_phone=F('company__phone'), company_logo=F('company__company_logo'), about_company=F('company__about_company'), company_site=F('company__company_site'), user_phone=F('phone')).first()
                companyDetail['first_name'] = user.first_name
                companyDetail['last_name'] = user.last_name
                if companyDetail['company_name'] != '' and companyDetail['company_name'] != None:
                    companyDetail['company'] = False
                    companyDetail['company_list'] = CompanyProfile.objects.all()
                else:
                    companyDetail['company'] = True
                return render(request, 'users/recruiterProfile.html', companyDetail)
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
            # "company_logo": request.FILES['company_logo'],
            "about_company": request.POST['about_company'],
            "company_site": request.POST.getlist('company_site'),
        }
        if 'company_logo' in request.FILES:
            company_details['company_logo'] = request.FILES['company_logo']
        if id:
            CompanyProfile.objects.filter(id=id).update(**company_details)
        else:
            CompanyProfile.objects.create(**company_details)
        return redirect('userprofile')
    if id == None:
        return render(request, 'users/editCompany.html', {'button': 'Save', 'page': 'Add'})
    else:
        companyProfile = CompanyProfile.objects.filter(id=id).first()
        return render(request, 'users/editCompany.html', {'data': companyProfile, 'button': 'Update', 'page': 'Edit'})
