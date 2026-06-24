from django.shortcuts import redirect


class SuperuserAdminGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)

        if path.startswith('/admin/'):
            return self.get_response(request)

        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        return redirect(f'/admin/login/?next={path}')