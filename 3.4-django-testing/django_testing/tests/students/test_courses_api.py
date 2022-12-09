import random

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

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
def test_api_retrieve(client, course_factory):
    courses = course_factory(_quantity=2)

    # Act
    response = client.get(f'/courses/{courses[0].id}/')
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data['id'] == courses[0].id


# @pytest.mark.django_db
# def test_api_list(client, course_factory):
#     courses = course_factory(_quantity=10)
#
#     # Act
#     response = client.get('/courses/')
#     data = response.json()
#
#     # Assert
#     assert response.status_code == 200
#     assert len(courses) == len(data)
#     for d, c in zip(data, courses):
#         assert d['id'] == c.id
#
#
# @pytest.mark.django_db
# def test_api_filter(client, course_factory):
#     n = 10
#     courses = course_factory(_quantity=n)
#
#     # Act
#     response = client.get('/courses/', data={id: random.randint(1, n)})
#     data = response.json()
#
#     # Assert
#     assert response.status_code == 200
#     assert data[0]['id'] in [course.id for course in courses]
#
#
# @pytest.mark.django_db
# def test_api_name_filter(client, course_factory):
#     n = 10
#     rand = random.randint(1, n)
#     courses = course_factory(_quantity=n)
#     name = courses[rand].name
#
#     # Act
#     response = client.get('/courses/', data={'name': name})
#     data = response.json()
#
#     # Assert
#     assert response.status_code == 200
#     assert data[0]['name'] in [course.name for course in courses]
#
#
# @pytest.mark.django_db
# def test_api_create(client):
#     name_ = 'Maksim'
#
#     # Act
#     request = client.post('/courses/', data={'name': name_})
#     load_data = request.json()
#     response = client.get('/courses/')
#     data = response.json()
#
#
#     # Assert
#     assert request.status_code == 201
#     assert response.status_code == 200
#     assert data[-1]['name'] == load_data['name']
#
#
# @pytest.mark.django_db
# def test_api_update(client):
#     name1 = 'Pithon_base'
#     name2 = 'Python'
#
#     # Act
#     request = client.post('/courses/', data={'name': name1})
#     num = request.json()['id']
#     update = client.put(f'/courses/{num}/', data={'name': name2})
#     upd = update.json()
#     response = client.get('/courses/')
#     data = response.json()
#
#
#     # Assert
#     assert request.status_code == 201
#     assert update.status_code == 200
#     assert response.status_code == 200
#     assert data[-1]['name'] == upd['name']
#
#
# @pytest.mark.django_db
# def test_api_delete(client):
#     name = 'Python'
#
#     # Act
#     request = client.post('/courses/', data={'name': name})
#     num = request.json()['id']
#     delete = client.delete(f'/courses/{num}/')
#     response = client.get('/courses/')
#     data = response.json()
#
#
#     # Assert
#     assert request.status_code == 201
#     assert delete.status_code == 204
#     assert response.status_code == 200
#     assert len(data) == 0
