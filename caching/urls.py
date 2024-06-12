from django.urls import path
from .views import employee, employee_with_out_caching, employee_with_radis_caching

urlpatterns = [
    path('employee/', employee, name='employee'),
    path("employee_without_caching/", employee_with_out_caching, name="without"),
    path("employee_with_radis_caching/", employee_with_radis_caching, name="radis_caching"),
]
