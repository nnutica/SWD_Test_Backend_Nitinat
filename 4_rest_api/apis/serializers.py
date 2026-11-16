from rest_framework import serializers

from .models import Classroom, School, Student, Teacher


class SchoolSerializer(serializers.ModelSerializer):
    """School fields for list, create and update."""

    class Meta:
        model = School
        fields = ["id", "name", "abbreviation", "address"]


class SchoolDetailSerializer(SchoolSerializer):
    """School with counts; the values come from annotate() in the view."""
    classroom_count = serializers.IntegerField(read_only=True)
    teacher_count = serializers.IntegerField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta(SchoolSerializer.Meta):
        fields = SchoolSerializer.Meta.fields + ["classroom_count", "teacher_count", "student_count"]


class ClassroomSerializer(serializers.ModelSerializer):
    """Classroom fields for list, create and update."""

    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]


class TeacherSummarySerializer(serializers.ModelSerializer):
    """Teacher without classrooms, for nesting inside a classroom."""

    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender"]


class StudentSummarySerializer(serializers.ModelSerializer):
    """Student without classroom, for nesting inside a classroom."""

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender"]


class ClassroomDetailSerializer(ClassroomSerializer):
    """Classroom with its teachers and students."""
    teachers = TeacherSummarySerializer(many=True, read_only=True)
    students = StudentSummarySerializer(many=True, read_only=True)

    class Meta(ClassroomSerializer.Meta):
        fields = ClassroomSerializer.Meta.fields + ["teachers", "students"]


class TeacherSerializer(serializers.ModelSerializer):
    """Teacher fields for list, create and update; classrooms are ids."""

    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender", "classrooms"]


class TeacherDetailSerializer(TeacherSerializer):
    """Teacher with full classroom objects instead of ids."""
    classrooms = ClassroomSerializer(many=True, read_only=True)


class StudentSerializer(serializers.ModelSerializer):
    """Student fields for list, create and update; classroom is an id."""

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "classroom"]


class StudentDetailSerializer(StudentSerializer):
    """Student with the full classroom object instead of its id."""
    classroom = ClassroomSerializer(read_only=True)
