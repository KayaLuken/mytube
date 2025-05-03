# tests/test_auth.py
import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestUserRegistration:
    def test_successful_registration(self, api_client):
        payload = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newemail@mail.com"
        }
        response = api_client.post("/auth/register/", payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_registration_with_missing_fields(self, api_client):
        payload = {
            "username": "newuser"
        }
        response = api_client.post("/auth/register/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        print(response.data)  # Debugging line to check the response data
        assert "password" in response.data
        assert "email" in response.data

    def test_registration_with_existing_username(self, api_client):
        User.objects.create_user(username="newuser", password="password123", email="existing@mail.com")
        payload = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newemail@mail.com"
        }
        response = api_client.post("/auth/register/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data


@pytest.mark.django_db
class TestUserLogin:
    def test_successful_login(self, api_client):
        User.objects.create_user(username="john", password="secret123")
        payload = {
            "username": "john",
            "password": "secret123"
        }
        response = api_client.post("/auth/login/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_with_invalid_credentials(self, api_client):
        User.objects.create_user(username="john", password="secret123")
        payload = {
            "username": "john",
            "password": "wrongpassword"
        }
        response = api_client.post("/auth/login/", payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credentials" in response.data["detail"]

    def test_login_with_nonexistent_user(self, api_client):
        payload = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = api_client.post("/auth/login/", payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credentials" in response.data["detail"]