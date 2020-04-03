import django.middleware.common as common
from utils import jsonify
import json


class CustomMiddleware(common.CommonMiddleware):
    def process_request(self, request):
        super(CustomMiddleware, self).process_request(request)
        if request.method == "OPTIONS" or request.path.startswith("/admin/"):
            return
        if request.body.decode():
            request.json = json.loads(request.body)

    def process_response(self, request, response):
        if request.path.startswith("/admin/"):
            return super().process_response(request, response)
        return super().process_response(request, jsonify(response))
