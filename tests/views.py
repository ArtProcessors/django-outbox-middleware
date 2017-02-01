from django.http import HttpResponse
from django.views.generic import View


class EchoView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse(request.body)
