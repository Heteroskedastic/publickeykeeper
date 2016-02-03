import random

from datetime import datetime, timedelta

from flask import session


def get_verify_code():
    now = datetime.now()
    # dummy
    expired = session.get('verify_code_exp')
    code = session.get('verify_code')
    if expired is None or expired < now:
        code = random.randint(100000, 999999)
        expired = now + timedelta(minutes=5)
        session['verify_code'] = code
        session['verify_code_exp'] = expired
    return {"code": code, "expired": expired}
