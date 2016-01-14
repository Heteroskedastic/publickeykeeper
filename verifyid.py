"""
Reminder, we are trying not to keep secrets.
Try to verify without keeping or knowing any secret.
"""

from random import randint
from twython import Twython

def twitter2(APP_KEY, access_token=ACCESS_TOKEN):
    """
    Only need to read to verify
    OAuth 2 (Application Authentication)
    """
    return Twython(APP_KEY, access_token=ACCESS_TOKEN)


def twitter_request(twitter_id):
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
        verifymsg = randint(1000000, 10000000)
        return instructions, verifymsg
    else:
        instructions = 'Post a status update on your twitter feed which includes exactly the following text'
        verifymsg = 'I have a new public key for secret twitter messages\n Check it out at https://publickeykeeper.org/twitter/{}'.format(twitter_id)
        return instructions, verifymsg


def twitter_verify(twitter_id, username, paid=False):
    """
    Need to check users twitter feed for the verify message. We will check the last 5 tweets
    :param twitter_id:
    :return: True/False
    """
    # TODO: make this work
    # TODO: This looks in useres timeline for the required verify text, When it is found users in marked verified.
    connection = twitter2(APP_KEY, access_token=ACCESS_TOKEN)
    if paid:
        msg = twitter.get_direct_messages(screen_name=username, count=1)
    else:
        msg = twitter.user_timeline(screen_name=username, count=5) # Look in the last 5 status updates.
    for