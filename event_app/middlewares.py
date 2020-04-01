import django.middleware.common as common
from utils import jsonify
import json


class CustomMiddleware(common.CommonMiddleware):
    def process_request(self, request):
        super(CustomMiddleware, self).process_request(request)
        if request.method == "OPTIONS":
            return
        if request.method != "POST":
            return jsonify(f"Method {request.method} not allowed", 501)
        request.json = json.loads(request.body)

    def process_response(self, request, response):
        return super().process_response(request, jsonify(response))
