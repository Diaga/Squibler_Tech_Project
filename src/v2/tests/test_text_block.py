from rest_framework import status
from rest_framework.test import APITestCase
from .. import models
from .. import serializers


class CreateTextBlockTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = models.User.objects.create(
            email='test@example.com', password='testpass'
        )
        self.user.set_password(self.user.password)
        self.user.save()

    def test_authenticated_and_owner(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/block/', data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        block = models.TextBlock.objects.filter(id=res.data['id']).first()
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

        permission_block = models.PermissionBlock.objects.filter(
            block=block, user=self.user
        ).first()
        self.assertEqual(permission_block.permission,
                         models.PermissionBlock.PermissionEnum.OWNER)

    def test_authenticated_and_editor(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        owner_user = models.User.objects.create(
            email='owner@example.com', password='testpass'
        )
        owner_user.set_password(owner_user.password)
        owner_user.save()

        owner_block = models.TextBlock.objects.create(
            **data
        )
        models.PermissionBlock.objects.create(
            block=owner_block, user=owner_user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        models.PermissionBlock.objects.create(
            block=owner_block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        data.update({'parent': str(owner_block.id)})
        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/block/', data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        editor_block = models.TextBlock.objects.filter(
            id=res.data['id']
        ).first()

        self.assertEqual(res.data, serializers.TextBlockSerializer(
            editor_block
        ).data)

    def test_authenticated_and_view(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        owner_user = models.User.objects.create(
            email='owner@example.com', password='testpass'
        )
        owner_user.set_password(owner_user.password)
        owner_user.save()

        owner_block = models.TextBlock.objects.create(
            **data
        )
        models.PermissionBlock.objects.create(
            block=owner_block, user=owner_user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        models.PermissionBlock.objects.create(
            block=owner_block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        data.update({'parent': str(owner_block.id)})
        self.client.force_authenticate(user=self.user)

        res = self.client.post('/v2/block/', data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        owner_user = models.User.objects.create(
            email='owner@example.com', password='testpass'
        )
        owner_user.set_password(owner_user.password)
        owner_user.save()

        owner_block = models.TextBlock.objects.create(
            **data
        )
        models.PermissionBlock.objects.create(
            block=owner_block, user=owner_user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        data.update({'parent': str(owner_block.id)})

        res = self.client.post('/v2/block/', data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
