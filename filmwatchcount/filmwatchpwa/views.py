from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
TEMPLATE_DIR = Path(__file__).parent / "templates/filmwatchpwa"
def manifest(request):
    response = render(request,"filmwatchpwa/manifest.webmanifest",content_type="application/manifest+json")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def serviceworker(request):
    response = render(request,"filmwatchpwa/pwabuilder-sw.js",content_type="application/javascript")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def serviceworker_register(request):
    response = render(request,"filmwatchpwa/sw_register.js",content_type="application/javascript")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def offline(request):
    return render(request,"filmwatchpwa/offline.html")
def date_list(request):
    details = {}
    for file in TEMPLATE_DIR.iterdir():
        details[file.name] = file.stat().st_mtime
    response = JsonResponse(details)
    response['cache-control'] = 'no-store'
    return response