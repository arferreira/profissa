from django.shortcuts import render

# Create your views here.

def profile_public(request):
    return render(request, 'profile_public.html')
