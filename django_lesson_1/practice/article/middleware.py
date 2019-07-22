from django.urls import reverse
from django.shortcuts import redirect

class LoginRequuiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
            # One-time configuration and initialization.

    def __call__(self, request):
            # Code to be executed for each request before
            # the view (and later middleware) are called.

        response = self.get_response(request)
        path = request.path_info
        article_created_path = reverse('create')
        if not request.user.is_authenticated and path == article_created_path:
            return redirect(reverse('login'))
        return response