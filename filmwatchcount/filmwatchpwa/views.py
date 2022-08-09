from django.shortcuts import render
def manifest(request):
    return render(request,"filmwatchpwa/manifest.json",content_type="application/manifest+json")
def serviceworker(request):
    return render(request,"filmwatchpwa/pwabuilder-sw.js",content_type="application/javascript")
def serviceworker_register(request):
    return render(request,"filmwatchpwa/sw_register.js",content_type="application/javascript")
def offline(request):
    return render(request,"filmwatchpwa/offline.html")