from django_filters import FilterSet, filters

from .models import Classroom, School, Student, Teacher

# Classroom.__str__ reads its school; join it so the browsable API's filter dropdown avoids N+1
CLASSROOM_CHOICES = Classroom.objects.select_related("school")


class SchoolFilter(FilterSet):
    """Filter schools by part of the name."""
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = School
        fields = ["name"]


class ClassroomFilter(FilterSet):
    """Filter classrooms by school id."""

    class Meta:
        model = Classroom
        fields = ["school"]


class TeacherFilter(FilterSet):
    """Filter teachers by school, classroom, name and gender."""
    # distinct: a teacher in two classrooms of the same school would otherwise appear twice
    school = filters.ModelChoiceFilter(
        field_name="classrooms__school", queryset=School.objects.all(), distinct=True,
    )
    classroom = filters.ModelChoiceFilter(
        field_name="classrooms", queryset=CLASSROOM_CHOICES, distinct=True,
    )
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Teacher
        fields = ["school", "classroom", "first_name", "last_name", "gender"]


class StudentFilter(FilterSet):
    """Filter students by school, classroom, name and gender."""
    school = filters.ModelChoiceFilter(field_name="classroom__school", queryset=School.objects.all())
    classroom = filters.ModelChoiceFilter(queryset=CLASSROOM_CHOICES)
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Student
        fields = ["school", "classroom", "first_name", "last_name", "gender"]
