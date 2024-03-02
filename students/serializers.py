from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    # def validate(self, data):
    #     course = Course.objects.filter(name=data.get("name"))
    #     course_students = course["students"]["id"]
    #     if course_students.count >= 20:
    #         for i in data.get("students")[id]:
    #             if i not in course_students:
    #                 raise serializers.ValidationError("К курсу прикреплено максимальное количество студентов")
    #     return data
