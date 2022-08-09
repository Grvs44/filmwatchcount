from django.shortcuts import render
def manifest(request):
    return render(request,"filmwatchpwa/manifest.json",content_type="application/json")
def serviceworker(request):
    return render(request,"filmwatchpwa/pwabuilder-sw.js",content_type="application/javascript")
def serviceworker_update(request):
    return render(request,"filmwatchpwa/pwabuilder-sw-update.js",content_type="application/javascript")
def offline(request):
    return render(request,"filmwatchpwa/offline.html")