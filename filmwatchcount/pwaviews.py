from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
TEMPLATE_DIR = Path(__file__).parent / "templates/filmwatchcount"
PWA_FILES = [Path(TEMPLATE_DIR / "manifest.webmanifest"),Path(TEMPLATE_DIR / "pwabuilder-sw.js"),Path(TEMPLATE_DIR / "sw_register.js"),Path(TEMPLATE_DIR / "offline.html")]
del TEMPLATE_DIR
def manifest(request):
    response = render(request,"filmwatchcount/manifest.webmanifest",content_type="application/manifest+json; charset=utf-8")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def serviceworker(request):
    response = render(request,"filmwatchcount/pwabuilder-sw.js",content_type="application/javascript; charset=utf-8")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def serviceworker_register(request):
    response = render(request,"filmwatchcount/sw_register.js",content_type="application/javascript; charset=utf-8")
    response['cache-control'] = 'public,max-age=31536000'
    return response
def offline(request):
    return render(request,"filmwatchcount/offline.html")
def date_list(request):
    details = []
    for file in PWA_FILES:
        details.append([file.name,file.stat().st_mtime])
    response = JsonResponse(details,safe=False)
    response['cache-control'] = 'no-store'
    return response