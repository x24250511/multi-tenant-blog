from blog.models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # Remove port if present
        tenant = Tenant.objects.filter(domain_url=host).first()
        request.tenant = tenant
        request.tenant = tenant
        return self.get_response(request)
