from django.contrib import admin
from django.conf.urls import include,url



# admin = A call to get the admin panel of django.
# ''    = To access the booker app urls.
# api   = To access the api calls.



urlpatterns = [
    url('admin/', admin.site.urls),
    url('', include('booker.urls')),
    url('^api/', include('api.urls')),
]
