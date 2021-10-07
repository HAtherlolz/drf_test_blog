from django.db import models


from blog.models import User


class Notification(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, db_index=True)
    send_date = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} type{self.type}"
