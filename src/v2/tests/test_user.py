from rest_framework import status
from rest_framework.test import APITestCase
from .. import models
from .. import serializers


class LoginTestCase(APITestCase):

    def test_correct_credentials(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpass'
        }

        user = models.User.objects.create(
            email=data['username'],
            password=data['password']
        )
        user.set_password(user.password)
        user.save()

        res = self.client.post('/v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, {
            'token': user.auth_token.key
        })

    def test_user_does_not_exist(self):
        data = {
            'username': 'no@example.com',
            'password': 'testpass'
        }

        res = self.client.post('/v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            "non_field_errors": [
                "Unable to log in with provided credentials."
            ]
        })

    def test_incorrect_credentials(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpass'
        }

        user = models.User.objects.create(
            email=data['username'],
            password=data['password']
        )
        user.set_password(user.password)
        user.save()

        data.update({'password': 'wrongpass'})
        res = self.client.post('/v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            "non_field_errors": [
                "Unable to log in with provided credentials."
            ]
        })


class CreateUserTestCase(APITestCase):

    def test_unauthenticated(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass'
        }

        res = self.client.post('/v2/user/', data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = models.User.objects.filter(email=data['email']).first()

        self.assertDictEqual(res.data, serializers.UserSerializer(user).data)

    def test_non_valid_email(self):
        data = {
            'email': 'test',
            'password': 'testpass'
        }

        res = self.client.post('/v2/user/', data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated(self):
        data = {
            'email': 'test@email.com',
            'password': 'testpass'
        }

        user = models.User.objects.create(
            email='test@example.com',
            password=data['password']
        )
        user.set_password(user.password)
        user.save()

        self.client.force_authenticate(user=user)

        res = self.client.post('/v2/user/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class RetrieveAuthenticatedUserTestCase(APITestCase):

    def test_authenticated(self):
        user = models.User.objects.create(
            email='test@example.com',
            password='testpass'
        )
        user.set_password(user.password)
        user.save()

        self.client.force_authenticate(user=user)

        res = self.client.get('/v2/user/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, serializers.UserSerializer(user).data)

    def test_unauthenticated(self):
        res = self.client.get('/v2/user/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUserByIdTestCase(APITestCase):

    def test_authenticated(self):
        user = models.User.objects.create(
            email='test@example.com',
            password='testpass'
        )
        user.set_password(user.password)
        user.save()

        self.client.force_authenticate(user=user)

        res = self.client.get(f'/v2/user/{user.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, serializers.UserSerializer(user).data)

    def test_unauthenticated(self):
        res = self.client.get('/v2/user/uuid/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_does_not_exist(self):
        user = models.User.objects.create(
            email='test@example.com',
            password='testpass'
        )
        user.set_password(user.password)
        user.save()

        self.client.force_authenticate(user=user)

        res = self.client.get('/v2/user/uuid/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
