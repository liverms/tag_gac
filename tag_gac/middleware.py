from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class CustomLangMiddleware(MiddlewareMixin):
    """This controls whether the french or english page
    is loaded.

    Args:
        MiddlewareMixin ([class]): MiddlewareMixin class
    """
    def process_request(self, request):
        if 'ouvert' in request.build_absolute_uri():
            language = 'fr'
        else:
            language = 'en'
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        translation.deactivate()
        return response