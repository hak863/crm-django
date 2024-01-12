from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect 

class OrganiserAndLoginRequiredMixin(AccessMixin): #this is the organiser and login required mixin class that inherits from the access mixin class
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs): #this is the dispatch function that takes in the request, args and kwargs
        if not request.user.is_authenticated or not request.user.is_organiser: #this checks if the user is authenticated and is an organiser
            return redirect("login") #this redirects the user to the login page
        return super().dispatch(request, *args, **kwargs) #this returns the super dispatch function with the request, args and kwargs