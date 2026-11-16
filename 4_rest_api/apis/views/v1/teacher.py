from rest_framework import viewsets

from apis.filters import TeacherFilter
from apis.models import Teacher
from apis.serializers import TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    """CRUD for teachers; detail shows full classroom objects."""
    # Every response lists the classrooms, so load them in one extra query instead of one per teacher
    queryset = Teacher.objects.prefetch_related("classrooms")
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return TeacherSerializer
