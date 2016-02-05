import json
from datetime import datetime

from flask import request, render_template, Response
from flask.views import MethodView

from api.utils import json_serial
from base.verifyid import VERIFY


class VVerify(MethodView):
    @staticmethod
    def verify_service(service, code):
        from db import PublicId
        p = PublicId.get(idtype=service, code=code)
        if p.code_expored_date < datetime.now():
            p.refresh_code()
            p = p.update_obj()
            p.resend_code()
            raise ValueError('Code expired')
        p.accept_veiry()
        Response(json.dumps({'status': 'ok'}, default=json_serial), status=200, mimetype="application/json")

    @staticmethod
    def get():
        if request.args.get('key'):
            return VVerify.verify_service(service=PublicId.EMAIL, code=request.args.get('key'))
        else:
            # dummy
            return render_template('test.html')

    @staticmethod
    def post():
        from api.tasks import twitter_verify
        from db import PublicId
        username = request.form.get('username')
        service = request.form.get('service')
        p = PublicId.get(idtype=service, account=username).refresh_code()

        twitter_verify.apply_async(kwargs=({"code": p.code,
                                            "username": username}),
                                   countdown=5)
        return Response(json.dumps({"text": VERIFY.format(p.code)}, default=json_serial), status=200, mimetype="application/json")
