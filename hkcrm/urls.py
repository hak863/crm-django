from django.contrib import admin
from django.urls import path, include
from leads.views import landing_page, LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls), #admin page
    path('', LandingPageView.as_view(), name='landing_page'), #points to landing page
    path('leads/', include('leads.urls', namespace="leads")) #points to leads/urls.py
]
