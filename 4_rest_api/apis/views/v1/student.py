from rest_framework import viewsets

from apis.filters import StudentFilter
from apis.models import Student
from apis.serializers import StudentDetailSerializer, StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """CRUD for students; detail shows the full classroom object."""
    queryset = Student.objects.all()
    filterset_class = StudentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.select_related("classroom")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer
        return StudentSerializer
