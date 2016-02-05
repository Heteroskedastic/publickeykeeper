"""
Reminder, we are trying not to keep secrets.
Try to verify without keeping or knowing any secret.
"""


from twython import Twython

import config

verify_start = 'I have a new public key for secret twitter messages at'
verify_site = 'https://publickeykeeper.org'
VERIFY = '{start} {site}. My verify code is: '.format(**{"start": verify_start, "site": verify_site}) + '{}'


class VerifyCore:
    pass


class TwitterVerify(VerifyCore):
    twitter = Twython(config.TWITTER_APP_KEY, config.TWITTER_APP_KEY_SECRET,
                      config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)

    def twitter_request(self, twitter_id, code):
        """
        Verify person has control of twitter account:
        Free accounts, Spead the word about PublicKeyKeeper.org
        twitter_id: Twitter ID user is trying to add a public key for.
        Free Accounts (status update):
            returns: Text for user to post as status update on twitter
        Paid (Direct Message):
            returns: Text for user to post as status update on twitter
        """
        # TODO: Make this work
        # TODO lookup if user is a paid user, for now all useer accounts are free (All are free now)
        paid = False
        if paid:
            instructions = 'send a direct messages to @publickeykeeper with the following random number in it.'
            verifymsg = VERIFY.format(code)
        else:
            instructions = 'Post a status update on your twitter feed which includes exactly the following text'
            verifymsg = VERIFY.format(code)

        return instructions, verifymsg

    def twitter_verify(self, code, twitter_id=None, username=None, paid=False):
        """
        Need to check users twitter feed for the verify message. We will check the last 5 tweets
        :param twitter_id:
        :return: True/False
        """
        if paid:
            msgs = self.twitter.get_direct_messages(screen_name=username, count=1)
        else:
            msgs = self.twitter.get_user_timeline(screen_name=username, count=5) # Look in the last 5 status updates.
        for msg in msgs:
            if msg["text"].startswith(verify_start):
                for url in msg['entities']["urls"]:
                    if verify_site in url['expanded_url'] and str(code) in msg["text"]:
                        return True
        return False
