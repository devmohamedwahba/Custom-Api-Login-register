from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def handler404(request, exception):
    logger.exception(f'Page not found error 404 {exception}')
    response = JsonResponse(data={'error': 'this endpoint is not found', 'status_code': 404})
    response.status_code = 404
    return response


def handler500(request):
    logger.exception('Internal Server Error 500')
    response = JsonResponse(data={'error': 'Server Error', 'status_code': 500})
    response.status_code = 500
    return response
