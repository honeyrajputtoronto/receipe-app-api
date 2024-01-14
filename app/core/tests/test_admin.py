"""Test for Django Admin modifications."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTest(TestCase):
    """Test for Django admin."""

    #setup code is going to run every single test that we add.
    def setUp(self):
        """create user and client."""
        # Django test client which that would allow us to make HTTP requests.
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password='sample123'
        )
        # this force login method allow us to force the authentication to this user. every request will be authenticated from this user.
        self.client.force_login(self.admin_user)
        # we can use this to test the listings
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='sample123',
            name='Test user'
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        # Get the page that will show the list of the users. from documentations, we got the url for the list of users.
        url = reverse('admin:core_user_changelist')

        #here we are getting an HTTP request to the url
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


    def test_create_user_page(self):
        """Test the add user page."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

