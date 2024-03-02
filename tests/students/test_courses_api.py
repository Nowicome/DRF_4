import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    # Course.objects.create(name="test")

    # Act
    response = client.get("/api/v1/courses/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    # assert data[0]["name"] == "test"


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c["name"] == courses[i].name


@pytest.mark.django_db
def test_get_courses_filter_id(client, course_factory):
    courses = course_factory(_quantity=7)

    response = client.get(f"/api/v1/courses/?id={courses[3].id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == courses[3].id


@pytest.mark.django_db
def test_get_courses_filter_name(client, course_factory):
    courses = course_factory(_quantity=15)

    response = client.get(f"/api/v1/courses/?name={courses[12].name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == courses[12].name


@pytest.mark.django_db
def test_create_course(client, course_factory):
    count = Course.objects.count()

    response = client.post("/api/v1/courses/", data={"name": "test", })

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(client, course_factory, student_factory):
    course_count = Course.objects.count()
    student_count = Student.objects.count()
    courses = course_factory(_quantity=1)
    students = student_factory(_quantity=1)

    response = client.patch(
        f"/api/v1/courses/{courses[0].id}/",
        data={
            "name": "test",
            "students": [
                f"{students[0].id}",
            ]
        }
    )

    assert response.status_code == 200
    assert Course.objects.count() == course_count + 1
    assert Student.objects.count() == student_count + 1
    data = response.json()
    assert data["name"] == "test"
    assert data["students"][0] == students[0].id


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=1)
    count = Course.objects.count()

    response = client.delete(f"/api/v1/courses/{courses[0].id}/")

    assert response.status_code == 204
    assert Course.objects.count() == count - 1


# def test_example():
#     assert False, "Just test example"
