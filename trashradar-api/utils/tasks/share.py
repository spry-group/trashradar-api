from utils.social_media.twitter import Twitter
from complaints.models import Complaint

from trashradar.celery import app


@app.task(name='share_complaint')
def share_complaint(complaint_id):
    """
    Share complaints on social networks
    :param complaint_id: integer Complaint Id to tweet
    :return: None
    """
    twitter = Twitter()
    complaint = Complaint.objects.get(pk=complaint_id)
    message = u'{} - {}'.format(
        complaint.entity.twitter,
        complaint.entity.template_message
    )
    complaint.tweet_status = twitter.tweet(message, complaint.picture)
    complaint.save()
