from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase
from .. import models
from .. import serializers


class CreatePermissionBlockTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            email='test@example.com', password='testpass'
        )
        self.user.set_password(self.user.password)
        self.user.save()

        self.block = models.TextBlock.objects.create(
            title='Intro', text='This document is ...',
        )

        self.other_user = models.User.objects.create(
            email='other@example.com', password='testpass'
        )
        self.other_user.set_password(self.other_user.password)
        self.other_user.save()

    def test_authenticated_and_owner(self):
        data = {
            'block': str(self.block.id),
            'user': str(self.other_user.id),
            'permission': models.PermissionBlock.PermissionEnum.EDITOR
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/permission/block/', data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        permission_block = models.PermissionBlock.objects.filter(
            id=res.data['id']
        ).first()
        self.assertDictEqual(res.data, serializers.PermissionBlockSerializer(
            permission_block
        ).data)

    def test_authenticated_and_editor(self):
        data = {
            'block': str(self.block.id),
            'user': str(self.other_user.id),
            'permission': models.PermissionBlock.PermissionEnum.EDITOR
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/permission/block/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_and_view(self):
        data = {
            'block': str(self.block.id),
            'user': str(self.other_user.id),
            'permission': models.PermissionBlock.PermissionEnum.EDITOR
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/permission/block/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated(self):
        data = {
            'block': str(self.block.id),
            'user': str(self.other_user.id),
            'permission': models.PermissionBlock.PermissionEnum.EDITOR
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/permission/block/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'block': str(self.block.id),
            'user': str(self.other_user.id),
            'permission': models.PermissionBlock.PermissionEnum.EDITOR
        }

        res = self.client.post('/v2/permission/block/', data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrievePermissionBlocksByBlockIdTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            email='test@example.com', password='testpass'
        )
        self.user.set_password(self.user.password)
        self.user.save()

        self.block = models.TextBlock.objects.create(
            title='Intro', text='This document is ...',
        )

        self.other_user = models.User.objects.create(
            email='other@example.com', password='testpass'
        )
        self.other_user.set_password(self.other_user.password)
        self.other_user.save()

    def test_authenticated_and_owner(self):
        permission_blocks = [
            models.PermissionBlock.objects.create(
                block=self.block, user=self.user,
                permission=models.PermissionBlock.PermissionEnum.OWNER
            ),
            models.PermissionBlock.objects.create(
                block=self.block, user=self.other_user,
                permission=models.PermissionBlock.PermissionEnum.EDITOR
            )
        ]

        self.client.force_authenticate(user=self.user)

        res = self.client.get('/v2/permission/block/', {
            'block': str(self.block.id)
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertListEqual(res.data, serializers.PermissionBlockSerializer(
            permission_blocks, many=True
        ).data)

    def test_authenticated_and_editor(self):
        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )
        models.PermissionBlock.objects.create(
            block=self.block, user=self.other_user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get('/v2/permission/block/', {
            'block': str(self.block.id)
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_and_view(self):
        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )
        models.PermissionBlock.objects.create(
            block=self.block, user=self.other_user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get('/v2/permission/block/', {
            'block': str(self.block.id)
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated(self):
        models.PermissionBlock.objects.create(
            block=self.block, user=self.other_user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get('/v2/permission/block/', {
            'block': str(self.block.id)
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        models.PermissionBlock.objects.create(
            block=self.block, user=self.other_user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        res = self.client.get('/v2/permission/block/', {
            'block': str(self.block.id)
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdatePermissionBlockByIdTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            email='test@example.com', password='testpass'
        )
        self.user.set_password(self.user.password)
        self.user.save()

        self.block = models.TextBlock.objects.create(
            title='Intro', text='This document is ...',
        )

        self.other_user = models.User.objects.create(
            email='other@example.com', password='testpass'
        )
        self.other_user.set_password(self.other_user.password)
        self.other_user.save()

        self.other_permission_block = models.PermissionBlock.objects.create(
            block=self.block, user=self.other_user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

    def test_authenticated_and_owner(self):
        data = {
            'permission': models.PermissionBlock.PermissionEnum.VIEW
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(
            f'/v2/permission/block/{self.other_permission_block.id}/', data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.other_permission_block.refresh_from_db()
        self.assertDictEqual(res.data, serializers.PermissionBlockSerializer(
            self.other_permission_block
        ).data)

    def test_authenticated_and_editor(self):
        data = {
            'permission': models.PermissionBlock.PermissionEnum.VIEW
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(
            f'/v2/permission/block/{self.other_permission_block.id}/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_and_view(self):
        data = {
            'permission': models.PermissionBlock.PermissionEnum.VIEW
        }

        models.PermissionBlock.objects.create(
            block=self.block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(
            f'/v2/permission/block/{self.other_permission_block.id}/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated(self):
        data = {
            'permission': models.PermissionBlock.PermissionEnum.VIEW
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(
            f'/v2/permission/block/{self.other_permission_block.id}/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'permission': models.PermissionBlock.PermissionEnum.VIEW
        }

        res = self.client.patch(
            f'/v2/permission/block/{self.other_permission_block.id}/', data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
