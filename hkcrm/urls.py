from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, include
from leads.views import landing_page, LandingPageView, SignupView, DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'), #this is the path for the landing page (crm-django/leads/templates/landing.html)
    path('dashboard/', DashboardView.as_view(), name='dashboard'), #this is the path for the dashboard page (crm-django/leads/templates/dashboard.html)
    path('leads/',  include('leads.urls', namespace="leads")), #this is the path for the leads page (crm-django/leads/templates/leads/lead_list.html)
    path('agents/',  include('agents.urls', namespace="agents")), #this is the path for the agents page (crm-django/agents/templates/agents/agent_list.html)
    path('signup/', SignupView.as_view(), name='signup'), #this is the path for the signup page (crm-django/leads/templates/signup.html)
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'), #this is the path for the reset password page (crm-django/leads/templates/registration/password_reset_form.html)
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'), #this is the path for the password reset done page (crm-django/leads/templates/registration/password_reset_done.html)
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), #this is the path for the password reset confirm page (crm-django/leads/templates/registration/password_reset_confirm.html)
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'), #this is the path for the password reset complete page (crm-django/leads/templates/registration/password_reset_complete.html)
    path('login/', LoginView.as_view(), name='login'), #this is the path for the login page (crm-django/leads/templates/registration/login.html)
    path('logout/', LogoutView.as_view(), name='logout'), #this is the path for the logout page (crm-django/leads/templates/registration/logged_out.html)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
