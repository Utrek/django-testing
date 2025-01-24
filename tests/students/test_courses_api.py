import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def courses_factory():
    def factory(*args,**kwargs):
        return baker.make(Course,*args,**kwargs)
    return factory

@pytest.fixture
def students_factory():
    def factory_s(*args,**kwargs):
        return baker.make(Student,*args,**kwargs)
    return factory_s

@pytest.mark.django_db
def test_get_first_course(client,courses_factory):
    course = courses_factory(_quantity=1, name= 'python')
    response = client.get("/api/v1/courses/")
    data = response.json()
    assert data[0]['name'] == course[0].name

@pytest.mark.django_db
def test_list_courses(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get("/api/v1/courses/")
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name

@pytest.mark.django_db
def test_id_filter_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/?id={courses[2].id}")
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == courses[2].id

@pytest.mark.django_db
def test_name_filter_course(client, courses_factory):
    courses = courses_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/?name={courses[1].name}")
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == courses[1].name  

@pytest.mark.django_db
def test_create_course(client):
    data = {"name": "Test Course"}
    response = client.post("/api/v1/courses/", data=data) 
    assert response.status_code == 201

@pytest.mark.django_db
def test_change_name_course(client, courses_factory):
    course = courses_factory(name='Math')
    url = f'/api/v1/courses/{course.id}/'
    data = {'name': 'Physics'}
    response = client.put(url, data)
    assert response.status_code == 200, 'PUT request should return 200 OK'
    course_new = Course.objects.get(id=course.id)
    assert course_new.name == data['name']

@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    course = courses_factory(name='Science')
    response = client.delete(f"/api/v1/courses/{course.id}/")
    
    assert response.status_code == 204
   
 


