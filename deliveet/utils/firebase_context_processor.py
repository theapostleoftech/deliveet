from django.conf import settings


def firebase_config(request):
    """
    This module adds firebase configuration to the request context.
    :param request:
    :return:
    """
    return {'firebase_config': settings.FIREBASE_CONFIG}
