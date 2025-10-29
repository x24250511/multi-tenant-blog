from blog.models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        try:
            request.tenant = Tenant.objects.get(domain=host)
        except Tenant.DoesNotExist:
            # fallback for localhost dev
            request.tenant = Tenant.objects.first()
        return self.get_response(request)
