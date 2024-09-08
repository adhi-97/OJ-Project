# logging_middleware.py

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestResponseLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        logger.info(f"Request: {request.method} {request.get_full_path()}")
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Body: {request.body}")

    def process_response(self, request, response):
        logger.info(f"Response: {response.status_code}")
        logger.info(f"Content: {response.content}")
        return response
