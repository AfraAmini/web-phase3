from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings



class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.META.get("HTTP_X_TOKEN", '') != '' :
            session_key = request.META.get("HTTP_X_TOKEN", '')
            request.session = self.SessionStore(session_key)
        else:
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
            request.session = self.SessionStore(session_key)
