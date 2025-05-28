import datetime

from django.http import HttpResponse, HttpResponseForbidden


class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'Noma’lum IP')
        now = datetime.datetime.now()
        print(f"[{now}] So‘rov IP: {ip}")
        print(request.META)

        response = self.get_response(request)
        return response

class LogUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user=request.META.get('HTTP_USER_AGENT','Unknown')
        print(user)
        response = self.get_response(request)
        return response


class WorkeerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.datetime.now().time()
        start_time = datetime.time(8, 0, 0)
        finish_time = datetime.time(18, 0, 0)

        if not (start_time <= now <= finish_time):
            return HttpResponseForbidden("sayt ishlamaydi")

        response = self.get_response(request)
        return response

import time
from django.http import HttpResponseRedirect

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 5
        self.time_window = 5
        self.last_requests = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = time.time()


        requests = self.last_requests.get(ip, [])
        requests = [req_time for req_time in requests if now - req_time < self.time_window]

        if len(requests) >= self.rate_limit:

            return HttpResponseRedirect('/slow-down/')


        requests.append(now)
        self.last_requests[ip] = requests

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Foydalanuvchi IP-manzilini aniqlash"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
