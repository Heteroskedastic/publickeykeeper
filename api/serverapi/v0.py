import json

from flask import Response, request
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


class VGetPubKey(VApiCore):
    @staticmethod
    def get():
        from db import Key
        account, service = request.form.get('account'), request.form.get('service')
        if not account:
            account, service = request.json.get('account'), request.json.get('service')
        key = Key.get_key(account, service)
        return Response(json.dumps({"key": key.publickey}, default=json_serial), status=200, mimetype="application/json")

    @staticmethod
    def post():
        pass
