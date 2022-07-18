from main.consumer import consumer
from threading import Timer

class RunConsumerMiddleware(object):
    def __init__(self, get_response):
        consumer()
        self.get_response = get_response

    def __call__(self, request):

        return self.get_response(request)
