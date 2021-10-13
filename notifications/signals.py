import environ


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from blog.models import User, Comment, UserFollowing
from .tasks import send_notification
from .models import Notification


env = environ.Env()

environ.Env.read_env()


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        notification_type = "New comment"
        subject = 'New comment under your post'
        message = f'You have new comment under your post from {user}'
        from_email = env('EMAIL_LOGIN')
        to_email = instance.post.user.email
        Notification.objects.create(user=user, type=notification_type)
        send_notification.delay(subject,
                          message, from_email, to_email)


@receiver(post_save, sender=UserFollowing)
def follow_made_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user_id
        notification_type = "New follow"
        subject = 'You have new follower'
        message = f'User {user} followed you, Now you can follow back'
        from_email = env('EMAIL_LOGIN')
        to_email = instance.user_id.email
        Notification.objects.create(user=user, type=notification_type)
        send_notification.delay(subject,
                          message, from_email, to_email)


@receiver(post_delete, sender=UserFollowing)
def unfollow_made_notification(sender, instance, **kwargs):
    user = instance.user_id
    notification_type = "New unfollow"
    subject = f'You have new unfollow'
    message = f'User {instance.following_user_id} unfollowed you.'
    from_email = env('EMAIL_LOGIN')
    to_email = instance.user_id.email
    Notification.objects.create(user=user, type=notification_type)
    send_notification.delay(subject,
                      message, from_email, to_email)


