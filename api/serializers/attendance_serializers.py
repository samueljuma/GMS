from rest_framework import serializers
from attendance.models import Attendance
from django.utils.timezone import now


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"

    def validate(self, data):
        """Ensure attendance is not marked twice for the same member on the same day."""
        member = data["member"]
        date = data.get("date", now().date())  # Default to today if no date is provided

        if not member:
            raise serializers.ValidationError({"member": "Member is required."})
        # Prevent marking attendance for future dates
        if date > now().date():
            raise serializers.ValidationError({"date": "Cannot mark attendance for a future date."})

        # Check if attendance already exists for that member and date
        if Attendance.objects.filter(member=member, date=date).exists():
            raise serializers.ValidationError({"attendance": "Attendance already marked for this date."})

        return data
