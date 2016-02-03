import json

from flask import Response
from flask.views import MethodView

from api.utils import json_serial
from .verify import get_verify_code


class VApiCore(MethodView):
    @staticmethod
    def get():
        """
        initial method
        :return: json
        """

        return "api base view"

    @staticmethod
    def post():
        """
        initial method
        :return: json
        """
        pass


class VVerify(VApiCore):
    @staticmethod
    def get():
        return Response(json.dumps(get_verify_code(), default=json_serial), status=200, mimetype="application/json")

    @staticmethod
    def post():
        """
        some verify info
        :return:
        """
        # TODO: running celery task
        pass
