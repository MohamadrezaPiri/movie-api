from .models import IpAddress


class GetIPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if not IpAddress.objects.filter(ip_address = ip).exists():
            ip_address = IpAddress.objects.create(ip_address = ip)
        else:
            ip_address = IpAddress.objects.get(ip_address=ip)    

        request.ip_address = ip_address             

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response