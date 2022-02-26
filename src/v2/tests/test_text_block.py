from django.db.models import ObjectDoesNotExist
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

        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
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

    def test_authenticated(self):
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


class RetrieveBlockByIdTestCase(APITestCase):

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

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

    def test_authenticated_and_editor(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

    def test_authenticated_and_view(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.get(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

    def test_authenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)

        self.client.force_authenticate(user=self.user)

        res = self.client.get(f'/v2/block/{block.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)

        res = self.client.get(f'/v2/block/{block.id}/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateBlockByIdTestCase(APITestCase):

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
        updated_data = {
            'title': 'Intro to platform',
            'text': 'That document was ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(f'/v2/block/{block.id}/', updated_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        block.refresh_from_db()
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

    def test_authenticated_and_editor(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }
        updated_data = {
            'title': 'Intro to platform',
            'text': 'That document was ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(f'/v2/block/{block.id}/', updated_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        block.refresh_from_db()
        self.assertDictEqual(res.data, serializers.TextBlockSerializer(
            block
        ).data)

    def test_authenticated_and_view(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }
        updated_data = {
            'title': 'Intro to platform',
            'text': 'That document was ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(f'/v2/block/{block.id}/', updated_data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }
        updated_data = {
            'title': 'Intro to platform',
            'text': 'That document was ...'
        }

        block = models.TextBlock.objects.create(**data)

        self.client.force_authenticate(user=self.user)

        res = self.client.patch(f'/v2/block/{block.id}/', updated_data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }
        updated_data = {
            'title': 'Intro to platform',
            'text': 'That document was ...'
        }

        block = models.TextBlock.objects.create(**data)

        res = self.client.patch(f'/v2/block/{block.id}/', updated_data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteBlockByIdTestCase(APITestCase):

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

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.OWNER
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            block.refresh_from_db()

    def test_authenticated_and_editor(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.EDITOR
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            block.refresh_from_db()

    def test_authenticated_and_view(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)
        models.PermissionBlock.objects.create(
            block=block, user=self.user,
            permission=models.PermissionBlock.PermissionEnum.VIEW
        )

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        data = {
            'title': 'Intro',
            'text': 'This document is ...'
        }

        block = models.TextBlock.objects.create(**data)

        res = self.client.delete(f'/v2/block/{block.id}/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
