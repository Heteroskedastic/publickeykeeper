import json

from flask import request, render_template, Response
from flask.views import MethodView

from api.serverapi.verify import get_verify_code
from api.utils import json_serial
from base.verifyid import VERIFY


class VTest(MethodView):
    @staticmethod
    def get():
        return render_template('test.html')

    @staticmethod
    def post():
        from api.tasks import twitter_verify
        username = request.form.get('username')
        code = get_verify_code()
        twitter_verify.apply_async(kwargs=({"code": code["code"],
                                            "username": username}),
                                   countdown=5)
        return Response(json.dumps({"text": VERIFY.format(code["code"])}, default=json_serial), status=200, mimetype="application/json")
