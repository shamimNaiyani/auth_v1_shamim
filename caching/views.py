from django.shortcuts import render
from .data import data as my_data
import time
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import Red

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def employee(request):
    
    
    # expensive database operation
    # Let assue it will take 10s
    time.sleep(10)
    
    return render(request, 'employee.html', {
        'employees': my_data
    })
    

def employee_with_out_caching(request):
    # expensive database operation
    # Let assue it will take 10s
    time.sleep(10)
    
    return render(request, 'employee.html', {
        'employees': my_data
    })


def employee_with_radis_caching(request):
    cache_data = Red.get("api")
    print("I called!")
    if cache_data:
        return render(request, 'employee.html', {
            'employees': cache_data
        })

    # expensive database operation
    # Let assue it will take 10s
    time.sleep(10) 
    res = my_data
    Red.set("api", my_data)
    return render(request, 'employee.html', {
        'employees': res
    })