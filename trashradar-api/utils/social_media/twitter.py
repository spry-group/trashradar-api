import twitter
from django.conf import settings


class Twitter(object):
    """
    Twitter class that will handle the connection between TrashRadar and
    the social network

    https://github.com/bear/python-twitter
    """

    def __init__(self):
        """
        Initialization of python-twitter
        """
        self.api = twitter.Api(
            consumer_key=settings.CONSUMER_KEY,
            consumer_secret=settings.CONSUMER_SECRET,
            access_token_key=settings.ACCESS_TOKEN_KEY,
            access_token_secret=settings.ACCESS_TOKEN_SECRET,
        )

    def tweet(self, message):
        """
        Creates a tweet on TrashRadar Twitter

        :param message: <string> Text to be submitted on Twitter
        :return: <array> Ids of the posted tweet
        """
        try:
            status = self.api.PostUpdate(message)
            return [status.id]
        except twitter.TwitterError:
            return []
