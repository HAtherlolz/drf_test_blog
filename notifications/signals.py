import environ


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail, BadHeaderError


from .models import Notification
from blog.models import User, Comment, UserFollowing


env = environ.Env()

environ.Env.read_env()


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        print("WWWOOOGOOOY")
        print("Created")
        user = instance.user
        notification_type = "New comment"
        subject = 'New comment under your post'
        message = f'You have new comment under your post from {user}'
        from_email = env('EMAIL_LOGIN')
        to_email = instance.post.user.email
        send_notification(user, notification_type, subject,
                          message, from_email, to_email)


@receiver(post_save, sender=UserFollowing)
def follow_made_notification(sender, instance, created, **kwargs):
    if created:
        print("WWWOOOGOOOY")
        print("Created")
        user = instance.user_id
        notification_type = "New follow"
        subject = 'You have new follower'
        message = f'User {user} followed you, Now you can follow back'
        from_email = env('EMAIL_LOGIN')
        to_email = instance.user_id.email
        send_notification(user, notification_type, subject,
                          message, from_email, to_email)


@receiver(post_delete, sender=UserFollowing)
def unfollow_made_notification(sender, instance, **kwargs):
    print("WWWOOOGOOOY")
    print("Created")
    user = instance.user_id
    notification_type = "New unfollow"
    subject = f'You have new unfollow'
    message = f'User {instance.following_user_id} unfollowed you.'
    from_email = env('EMAIL_LOGIN')
    to_email = instance.user_id.email
    send_notification(user, notification_type, subject,
                      message, from_email, to_email)


def send_notification(user, notification_type, subject,
                      message, from_email, to_email):
    print("Works")
    send_mail(subject, message, from_email,
                    [to_email, ])
    Notification.objects.create(user=user, type=notification_type)

