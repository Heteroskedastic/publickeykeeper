import json

from flask import Response, request
from flask.views import MethodView

from base.models import PublicId
from base.utils import json_serial, get_object_or_404
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
        account, service = request.form.get('account'), request.form.get('service')
        if not account:
            account, service = request.json.get('account'), request.json.get('service')
        publicid = get_object_or_404(PublicId, PublicId.account == account, PublicId.idtype == service)
        return Response(json.dumps({"key": publicid.key.first().publickey}, default=json_serial), status=200, mimetype="application/json")

    @staticmethod
    def post():
        pass
