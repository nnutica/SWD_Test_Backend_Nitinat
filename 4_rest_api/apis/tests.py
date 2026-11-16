from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Classroom, School, Student, Teacher


class BaseAPITestCase(APITestCase):
    """Shared data: two schools, three classrooms, two teachers, three students."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="tester", password="pass1234")

        cls.school_a = School.objects.create(name="Alpha Academy", abbreviation="AA", address="Bangkok")
        cls.school_b = School.objects.create(name="Beta School", abbreviation="BS", address="Chiang Mai")

        cls.room_a1 = Classroom.objects.create(school=cls.school_a, grade=1, section=1)
        cls.room_a2 = Classroom.objects.create(school=cls.school_a, grade=1, section=2)
        cls.room_b1 = Classroom.objects.create(school=cls.school_b, grade=1, section=1)

        # teacher_somchai teaches two rooms in the same school, to check distinct counts and filters
        cls.teacher_somchai = Teacher.objects.create(first_name="Somchai", last_name="Jaidee", gender="male")
        cls.teacher_somchai.classrooms.set([cls.room_a1, cls.room_a2])
        cls.teacher_malee = Teacher.objects.create(first_name="Malee", last_name="Rakdee", gender="female")
        cls.teacher_malee.classrooms.set([cls.room_b1])

        cls.student_nida = Student.objects.create(
            first_name="Nida", last_name="Suksai", gender="female", classroom=cls.room_a1,
        )
        cls.student_anan = Student.objects.create(
            first_name="Anan", last_name="Mekdee", gender="male", classroom=cls.room_a2,
        )
        cls.student_krit = Student.objects.create(
            first_name="Krit", last_name="Suksai", gender="male", classroom=cls.room_b1,
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)
        # Ask for JSON: the browsable renderer comes first in settings and turns 204 into 200
        self.client.credentials(HTTP_ACCEPT="application/json")

    def ids(self, response):
        """Return the ids in a list response, to compare results in one line."""
        return [item["id"] for item in response.data]


class AuthTests(BaseAPITestCase):
    """The scaffold settings require login on every endpoint."""

    def test_anonymous_request_is_rejected(self):
        self.client.force_authenticate(user=None)
        for name in ["school", "classroom", "teacher", "student"]:
            response = self.client.get(reverse(f"v1:{name}-list"))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, name)


class SchoolTests(BaseAPITestCase):

    def test_create(self):
        data = {"name": "Gamma School", "abbreviation": "GS", "address": "Phuket"}
        response = self.client.post(reverse("v1:school-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(School.objects.filter(name="Gamma School").exists())

    def test_create_without_required_fields_returns_400(self):
        response = self.client.post(reverse("v1:school-list"), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"name", "abbreviation", "address"})

    def test_list(self):
        response = self.client.get(reverse("v1:school-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ids(response), [self.school_a.id, self.school_b.id])

    def test_filter_by_name_is_case_insensitive_partial_match(self):
        response = self.client.get(reverse("v1:school-list"), {"name": "alpha"})
        self.assertEqual(self.ids(response), [self.school_a.id])

    def test_detail_has_counts(self):
        response = self.client.get(reverse("v1:school-detail", args=[self.school_a.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["classroom_count"], 2)
        self.assertEqual(response.data["teacher_count"], 1)  # Somchai once, though he has two rooms
        self.assertEqual(response.data["student_count"], 2)

    def test_detail_counts_use_a_single_query(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("v1:school-detail", args=[self.school_a.id]))

    def test_detail_of_missing_school_returns_404(self):
        response = self.client.get(reverse("v1:school-detail", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        url = reverse("v1:school-detail", args=[self.school_a.id])
        response = self.client.patch(url, {"address": "Nonthaburi"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school_a.refresh_from_db()
        self.assertEqual(self.school_a.address, "Nonthaburi")

    def test_delete_removes_its_classrooms_and_students_but_keeps_teachers(self):
        response = self.client.delete(reverse("v1:school-detail", args=[self.school_a.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Classroom.objects.filter(school_id=self.school_a.id).exists())
        self.assertFalse(Student.objects.filter(id=self.student_nida.id).exists())
        self.assertTrue(Teacher.objects.filter(id=self.teacher_somchai.id).exists())


class ClassroomTests(BaseAPITestCase):

    def test_create(self):
        data = {"school": self.school_b.id, "grade": 2, "section": 1}
        response = self.client.post(reverse("v1:classroom-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_room_in_same_school_returns_400(self):
        data = {"school": self.school_a.id, "grade": 1, "section": 1}
        response = self.client.post(reverse("v1:classroom-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_grade_zero_returns_400(self):
        data = {"school": self.school_a.id, "grade": 0, "section": 3}
        response = self.client.post(reverse("v1:classroom-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("grade", response.data)

    def test_filter_by_school(self):
        response = self.client.get(reverse("v1:classroom-list"), {"school": self.school_a.id})
        self.assertEqual(self.ids(response), [self.room_a1.id, self.room_a2.id])

    def test_filter_by_unknown_school_returns_400(self):
        response = self.client.get(reverse("v1:classroom-list"), {"school": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_lists_teachers_and_students(self):
        with self.assertNumQueries(3):  # classroom, its teachers, its students
            response = self.client.get(reverse("v1:classroom-detail", args=[self.room_a1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([t["id"] for t in response.data["teachers"]], [self.teacher_somchai.id])
        self.assertEqual([s["id"] for s in response.data["students"]], [self.student_nida.id])

    def test_update(self):
        url = reverse("v1:classroom-detail", args=[self.room_a2.id])
        response = self.client.patch(url, {"section": 5}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room_a2.refresh_from_db()
        self.assertEqual(self.room_a2.section, 5)

    def test_delete(self):
        response = self.client.delete(reverse("v1:classroom-detail", args=[self.room_b1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Classroom.objects.filter(id=self.room_b1.id).exists())


class TeacherTests(BaseAPITestCase):

    def test_create_with_classrooms(self):
        data = {
            "first_name": "Wichai", "last_name": "Dee", "gender": "male",
            "classrooms": [self.room_a1.id, self.room_b1.id],
        }
        response = self.client.post(reverse("v1:teacher-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        teacher = Teacher.objects.get(id=response.data["id"])
        self.assertEqual(set(teacher.classrooms.values_list("id", flat=True)), {self.room_a1.id, self.room_b1.id})

    def test_create_with_invalid_gender_returns_400(self):
        data = {"first_name": "X", "last_name": "Y", "gender": "robot"}
        response = self.client.post(reverse("v1:teacher-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("gender", response.data)

    def test_list_avoids_n_plus_one(self):
        with self.assertNumQueries(2):  # teachers, then all their classrooms at once
            self.client.get(reverse("v1:teacher-list"))

    def test_filter_by_school_returns_each_teacher_once(self):
        response = self.client.get(reverse("v1:teacher-list"), {"school": self.school_a.id})
        self.assertEqual(self.ids(response), [self.teacher_somchai.id])

    def test_filter_by_classroom(self):
        response = self.client.get(reverse("v1:teacher-list"), {"classroom": self.room_b1.id})
        self.assertEqual(self.ids(response), [self.teacher_malee.id])

    def test_filter_by_names_and_gender(self):
        url = reverse("v1:teacher-list")
        self.assertEqual(self.ids(self.client.get(url, {"first_name": "som"})), [self.teacher_somchai.id])
        self.assertEqual(self.ids(self.client.get(url, {"last_name": "rak"})), [self.teacher_malee.id])
        self.assertEqual(self.ids(self.client.get(url, {"gender": "female"})), [self.teacher_malee.id])

    def test_detail_lists_classrooms(self):
        response = self.client.get(reverse("v1:teacher-detail", args=[self.teacher_somchai.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([c["id"] for c in response.data["classrooms"]], [self.room_a1.id, self.room_a2.id])
        self.assertEqual(response.data["classrooms"][0]["grade"], 1)

    def test_update_classrooms(self):
        url = reverse("v1:teacher-detail", args=[self.teacher_malee.id])
        response = self.client.patch(url, {"classrooms": [self.room_a1.id]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.teacher_malee.classrooms.values_list("id", flat=True)), [self.room_a1.id])

    def test_delete_keeps_classrooms(self):
        response = self.client.delete(reverse("v1:teacher-detail", args=[self.teacher_somchai.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Classroom.objects.filter(id=self.room_a1.id).exists())


class StudentTests(BaseAPITestCase):

    def test_create(self):
        data = {"first_name": "Pim", "last_name": "Dee", "gender": "female", "classroom": self.room_a1.id}
        response = self.client.post(reverse("v1:student-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_classroom_returns_400(self):
        data = {"first_name": "Pim", "last_name": "Dee", "gender": "female"}
        response = self.client.post(reverse("v1:student-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("classroom", response.data)

    def test_filter_by_school(self):
        response = self.client.get(reverse("v1:student-list"), {"school": self.school_a.id})
        self.assertEqual(self.ids(response), [self.student_nida.id, self.student_anan.id])

    def test_filter_by_classroom(self):
        response = self.client.get(reverse("v1:student-list"), {"classroom": self.room_a2.id})
        self.assertEqual(self.ids(response), [self.student_anan.id])

    def test_filter_by_names_and_gender(self):
        url = reverse("v1:student-list")
        self.assertEqual(self.ids(self.client.get(url, {"first_name": "NI"})), [self.student_nida.id])
        self.assertEqual(
            self.ids(self.client.get(url, {"last_name": "suksai"})), [self.student_nida.id, self.student_krit.id],
        )
        self.assertEqual(
            self.ids(self.client.get(url, {"gender": "male"})), [self.student_anan.id, self.student_krit.id],
        )

    def test_filters_combine(self):
        params = {"school": self.school_a.id, "gender": "male"}
        response = self.client.get(reverse("v1:student-list"), params)
        self.assertEqual(self.ids(response), [self.student_anan.id])

    def test_detail_has_classroom_object(self):
        with self.assertNumQueries(1):  # student joined with classroom
            response = self.client.get(reverse("v1:student-detail", args=[self.student_nida.id]))
        self.assertEqual(response.data["classroom"]["id"], self.room_a1.id)
        self.assertEqual(response.data["classroom"]["section"], 1)

    def test_update_moves_student_to_another_classroom(self):
        url = reverse("v1:student-detail", args=[self.student_nida.id])
        response = self.client.patch(url, {"classroom": self.room_a2.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_nida.refresh_from_db()
        self.assertEqual(self.student_nida.classroom, self.room_a2)

    def test_delete(self):
        response = self.client.delete(reverse("v1:student-detail", args=[self.student_krit.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student_krit.id).exists())
