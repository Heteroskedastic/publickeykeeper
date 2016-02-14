import json

from flask import Response, request
from flask.views import MethodView

from base.models import PublicId, Message
from base.utils import json_serial, get_object_or_404
from .verify import get_verify_code


class VApiCore(MethodView):
    def get(self):
        """
        initial method
        :return: json
        """

        return "api base view"

    def post(self):
        """
        initial method
        :return: json
        """
        pass


class VVerify(VApiCore):
    def verify_email(self, key):
        p = PublicId.query.filter_by(code=key).first()
        if not p:
            return Response(json.dumps({"status": "error", "message": "User doesn't exist"}), status=500, mimetype="application/json")
        p.accept_verify()
        return Response(json.dumps({"status": "ok", "message": "verify completed"}), status=200, mimetype="application/json")

    def get(self):
        if request.args.get('key'):
            return self.verify_email(request.args.get('key'))
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


class VMessageEncrypt(VApiCore):
    @staticmethod
    def post():
        msg = Message(request.form.get('message') or request.json.get('message'))
        return Response(json.dumps({'message': msg.encrypt(), 'type': 'encrypt'}), mimetype='application/json')


class VMessageDecrypt(VApiCore):
    @staticmethod
    def post():
        msg = Message(request.form.get('message') or request.json.get('message'))
        return Response(json.dumps({'message': msg.decrypt(), 'type': 'decrypt'}), mimetype='application/json')
