from django.contrib import admin

from .models import Classroom, School, Student, Teacher

admin.site.register([School, Classroom, Teacher, Student])
