from django.db.models import Count
from rest_framework import viewsets

from apis.filters import SchoolFilter
from apis.models import School
from apis.serializers import SchoolDetailSerializer, SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    """CRUD for schools; detail adds classroom, teacher and student counts."""
    queryset = School.objects.all()
    filterset_class = SchoolFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            # One query for all counts; distinct because the joins repeat rows
            queryset = queryset.annotate(
                classroom_count=Count("classrooms", distinct=True),
                teacher_count=Count("classrooms__teachers", distinct=True),
                student_count=Count("classrooms__students", distinct=True),
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SchoolDetailSerializer
        return SchoolSerializer
