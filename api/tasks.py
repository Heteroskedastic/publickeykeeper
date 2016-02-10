from base.models import PublicId
from base.verifyid import TwitterVerify
from base import celery


@celery.task(bind=True, max_retries=15)
def twitter_verify(self, code, twitter_id=None, username=None, paid=False):
    verify = TwitterVerify()
    try:
        if verify.twitter_verify(code, twitter_id, username, paid):
            PublicId.get(account=username, idtype=PublicId.TWITTER).accept_verify()
            return True
        else:
            raise Exception("Message doesn't found")
    except Exception as exc:
        raise self.retry(countdown=20, exc=exc)
