from rest_framework import status
from rest_framework.test import APITestCase
from .. import models


class UserLoginTestCases(APITestCase):

    def test_correct_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass'
        }

        user = models.User.objects.create(**data)
        user.set_password(user.password)
        user.save()

        res = self.client.post('v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, {
            'token': user.token.key
        })

    def test_user_does_not_exist(self):
        data = {
            'email': 'no@example.com',
            'password': 'testpass'
        }

        res = self.client.post('v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'message': 'authentication failed'
        })

    def test_incorrect_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass'
        }

        user = models.User.objects.create(**data)
        user.set_password(user.password)
        user.save()

        data.update({'password': 'wrongpass'})
        res = self.client.post('v2/auth/login/', data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(res.data, {
            'message': 'authentication failed'
        })
