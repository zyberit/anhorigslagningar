from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .slagningar import loadfile
from .models import Case, Slagningar

# Create your views here.

def bootstrap(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
        loadfile(request.FILES['bootfile'])
        return redirect('/admin')
    else:
        form = UploadFileForm()
    return render(request, 'laddafil.html', {'form': form})


def signatur(request,signatur):
    case_list = Case.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'signatur.html', context)

def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)
    return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return redirect('/admin')
#     return render_to_response('home.html')
    return render(request,'home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')



