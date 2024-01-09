from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from leads.views import landing_page, LandingPageView, SignupView
from leads.views import LandingPageView


urlpatterns = [
    path('admin/', admin.site.urls), #admin page
    path('', LandingPageView.as_view(), name='landing-page'), #points to landing page
    path('leads/', include('leads.urls', namespace="leads")), #points to leads/urls.py
    path('agents/', include('agents.urls', namespace="agents")),
    path('login/', LoginView.as_view(), name="login"), #points to login page
    path('logout/', LogoutView.as_view(), name="logout"), #points to logout page
    path('signup/', SignupView.as_view(), name="signup")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
