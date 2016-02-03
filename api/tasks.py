from publickeykeeper import celery

from base.verifyid import TwitterVerify


@celery.task(bind=True, max_retries=15)
def twitter_verify(self, code, twitter_id=None, username=None, paid=False):
    verify = TwitterVerify()
    try:
        if verify.twitter_verify(code, twitter_id, username, paid):
            return True
        else:
            raise Exception("Message doesn't found")
    except Exception as exc:
        raise self.retry(countdown=20, exc=exc)
