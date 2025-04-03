from rest_framework import views, status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from attendance.models import Attendance
from api.utils.permissions import IsStaff
from api.serializers.attendance_serializers import AttendanceSerializer
from django.utils.timezone import now

class MarkAttendanceView(APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        requesting_user = request.user

        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = serializer.validated_data["member"]
        date = serializer.validated_data.get("date", now().date())
        if not date:
            date = now().date()

        attendance, created = Attendance.objects.get_or_create(
            member=member,
            date=date,
            defaults={"marked_by": requesting_user}  #Avoids duplicate marking
        )

        if not created:
            return Response(
                {"error": "Attendance already marked for this date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": f"Attendance marked for {member} successfully",
                "attendance_details": AttendanceSerializer(attendance).data
            },
            status=status.HTTP_201_CREATED
        )

# Fetch Attendance from db
class FetchAttendance(generics.ListAPIView): 
    queryset = Attendance.objects.all()
    permission_classes = [IsStaff]
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["date"]

class FetchAttendancForMember(APIView): ...