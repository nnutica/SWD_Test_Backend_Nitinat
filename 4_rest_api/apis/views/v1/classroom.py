from rest_framework import viewsets

from apis.filters import ClassroomFilter
from apis.models import Classroom
from apis.serializers import ClassroomDetailSerializer, ClassroomSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    """CRUD for classrooms; detail adds the lists of teachers and students."""
    queryset = Classroom.objects.all()
    filterset_class = ClassroomFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("teachers", "students")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return ClassroomSerializer
