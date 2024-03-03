from django.shortcuts import render


def about(request):
    return render(request, 'about.html')


def handler404(request, *args, **argv):
    return render(request, "404.html")
