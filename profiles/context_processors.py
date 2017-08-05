from django.conf import settings


def login_url(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'LOGIN_URL': settings.LOGIN_URL}
