import twitter
from tweetsplitter import split_tweet

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

    def tweet(self, message, media=None):
        """
        Creates a tweet on TrashRadar Twitter

        :param message: <string> Text to be submitted on Twitter
        :param media: <string> URL of the image to be sent on the Tweet
        :return: <array> Ids of the posted tweet
        """
        statuses = []
        messages = split_tweet(message)
        for i, tweet_content in enumerate(messages):
            extra_content = {}
            try:
                if media and i == len(messages) - 1:
                    extra_content['media'] = media
                status = self.api.PostUpdate(tweet_content, **extra_content)
                statuses.append(status.id)
            except twitter.TwitterError:
                pass
        return statuses
