from django.db import models
from users.models import CustomUser
from django.utils.timezone import now


def get_today():
    return now().date()

class Attendance(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=get_today,db_index=True)
    present = models.BooleanField(default=True)
    check_in_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    marked_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="marked_attendance", null=True, blank=True)
    
    class Meta:
        unique_together = ("member", "date")
