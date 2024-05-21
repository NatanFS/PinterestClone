from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Pin

class PinViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, username='testuser', password='testpass')
        self.user.set_password('testpass') 
        self.user.save()
        
        self.other_user = baker.make(User, username='otheruser', password='otherpass')
        self.other_user.set_password('otherpass')
        self.other_user.save()

        image = Image.new('RGB', (100, 100), color='red')
        temp_file = io.BytesIO()
        image.save(temp_file, format='JPEG')
        temp_file.seek(0)

        self.image_file = SimpleUploadedFile("test_image.jpg", temp_file.getvalue(), content_type="image/jpeg")
        
        self.pin = baker.make(Pin, user=self.user, image=self.image_file)
        self.pin_url = reverse('pin-detail', kwargs={'pk': self.pin.pk})
        self.like_url = reverse('pin-like', kwargs={'pk': self.pin.pk})

    def test_create_pin(self):
        self.client.force_login(self.user)
        url = reverse('pin-list')
        
        image = Image.new('RGB', (100, 100), color='red')
        temp_file = io.BytesIO()
        image.save(temp_file, format='JPEG')
        temp_file.seek(0)
        image_file = SimpleUploadedFile("new_test_image.jpg", temp_file.getvalue(), content_type="image/jpeg")

        data = {
            'title': 'New Pin',
            'description': 'A new test pin',
            'image': image_file,
        }
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(Pin.objects.count(), 2)
        self.assertEqual(Pin.objects.get(id=response.data['id']).title, 'New Pin')


    def test_like_pin(self):
        self.client.force_login(self.user)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.data['likes'], 1)
        self.assertEqual(response.data['liked'], True)

    def test_unlike_pin(self):
        self.client.force_login(self.user)
        self.client.post(self.like_url)  # Like the pin first
        response = self.client.post(self.like_url)  # Unlike the pin
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.data['likes'], 0)
        self.assertEqual(response.data['liked'], False)

    def test_permissions(self):
        # Test that a non-authenticated user cannot create a pin
        url = reverse('pin-list')
        data = {
            'title': 'New Pin',
            'description': 'A new test pin',
            'image': 'pins/new_test_image.jpg',
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test that a non-authenticated user cannot like a pin
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_pins(self):
        # Create a few more pins
        baker.make(Pin, user=self.user, image=self.image_file, tags='tag1,tag2')
        baker.make(Pin, user=self.other_user, image=self.image_file)
        
        url = reverse('pin-list')
        # Test filtering by user
        response = self.client.get(url, {'user': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(len(response.data['results']), 2)  # Two pins by testuser

        # Test filtering by title
        response = self.client.get(url, {'title': self.pin.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.pin.title)

        # Test filtering by tag
        response = self.client.get(url, {'tags': 'tag1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(len(response.data['results']), 1)
