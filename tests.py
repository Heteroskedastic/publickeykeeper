import json
import os
import random
import unittest

from flask.ext.testing import TestCase
from sqlalchemy.exc import IntegrityError

os.environ["DIAG_CONFIG_MODULE"] = "config.test"
os.environ["SECRET_KEY"] = str(random.randint(100000, 9999999))

from base import app, db
from base.models import User, PublicId, Key, Message


class PKKTests(TestCase):
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # db_path = os.path.join(basedir, 'config/test.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.key_text = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA/YCbN2eau8hwpMrq5J4wLIWdmajP9rEhMx4N5DlUqx6IwbikkJabMrZDXoH57Hqy0IdfwOMh102ggwo7dzG99uKCJVnhlpvBo9IfFbgdHeFBwnDXP/qT1XMOM9oiXHlsiqtpC7aycPqJo7XibhGaOTysyTFdhDnsuIsbliFWTrpT52DbNXFkhqWaGozRbD2D7wTVkeWPGoRNqkCn77GvBkz+KI6ghA8ktsrA2HOCnLnllwJvWNlpQZIkZcm7ksPb+sBjVxUIiz4b3z/xBxGceLcJkA//pV+a8GcubCl0GtKhTdncFWpoMat0JIJmFk3NZZeOq+1UIkXQ9gFjZp5FPwIDAQAB'
        self.user = User(firstname="admin", lastname="admin", active=True, login="admin")
        db.session.add(self.user)
        db.session.commit()
        self.publicid = PublicId(idtype=PublicId.TWITTER, account="user", user_id=self.user.id, verifyed=True, code="my_code")
        self.publicid_email = PublicId(idtype=PublicId.EMAIL, account="user", user_id=self.user.id, verifyed=True, code="my_code")
        db.session.add(self.publicid)
        db.session.add(self.publicid_email)
        db.session.commit()
        self.key = Key(publicid_id=self.publicid.id, keytype=Key.RSA, publickey=self.key_text)
        db.session.add(self.key)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # os.remove(self.db_path)

    def test_home_data(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b"Hello World! from the index")

    def test_user(self):
        u = User(firstname="admin", lastname="admin", active=True, login="admin1")
        db.session.add(u)
        db.session.commit()
        assert u in db.session
        try:
            u = User(firstname="admin", lastname="admin", active=True, login="admin1")
            db.session.add(u)
            db.session.commit()
            assert False
        except IntegrityError:
            assert True

    def test_publicid(self):
        p = PublicId(idtype=PublicId.TWITTER, account="user1", user_id=self.user.id, verifyed=True)
        db.session.add(p)
        db.session.commit()
        p = PublicId(idtype=PublicId.EMAIL, account="user1", user_id=self.user.id, verifyed=True, code="my_code")
        db.session.add(p)
        db.session.commit()
        old_code = p.code
        p.refresh_code()
        assert p.code != old_code

    def test_key(self):
        k = Key(publicid_id=self.publicid.id, keytype=Key.RSA, publickey=self.key_text + 'a')
        db.session.add(k)
        db.session.commit()

    def test_verify_email(self):
        p = PublicId(idtype=PublicId.EMAIL, account="user@publickeykeeper.org", user_id=self.user.id)
        db.session.add(p)
        db.session.commit()
        p.refresh_code()
        url = '/api/verify?key={}'.format(p.code)
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('ascii'))
        assert data["message"] == "verify completed"
        assert p.verifyed

if __name__ == '__main__':
    unittest.main()
