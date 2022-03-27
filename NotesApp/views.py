from django.shortcuts import render

# Create your views here.
def prepIndex(request):
    return render(request, 'prepup/index.html')


def interviewIndex(request):
    return render(request, 'prepup/interviewPrep.html')