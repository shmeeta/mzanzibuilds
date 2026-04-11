from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserProfileTests(TestCase):
    # create a user to check if profile is automatically created
    def setUp(self): 
        self.user = User.objects.create_user(username='johndoe', password='password123')
        self.other_user = User.objects.create_user(username='janedoe', password='password123')

    def test_signal_creates_profile(self):
        # Check if profile exists for user created in setup
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.profile.bio, 'No Bio yet.')


    #  check if profile page loads for an authenticated user
    def test_profile_view_accessible(self):
        self.client.login(username='johndoe', password='password123')
        url = reverse('profile_page', kwargs={'username': 'johndoe'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'johndoe')

    def test_edit_profile_submission(self):
        """Tests if the profile update form saves data correctly"""
        self.client.login(username='johndoe', password='password123')
        url = reverse('edit_profile')
        
        #new profile data
        payload = {
            'bio': 'Software Engineer from Johannesburg',
            'location': 'Johannesburg',
            'profession': 'Developer'
        }
        response = self.client.post(url, payload)
        
        # Refresh from db
        self.user.profile.refresh_from_db()
        
        # Check if redirect is correct
        self.assertRedirects(response, reverse('profile_page', kwargs={'username': 'johndoe'}))
        # Check if data saved
        self.assertEqual(self.user.profile.bio, 'Software Engineer from Joburg')
        self.assertEqual(self.user.profile.location, 'Johannesburg')

    def test_profile_view_requires_login(self):
        # test so anon users can't see profile info
        url = reverse('profile_page', kwargs={'username': 'johndoe'})
        response = self.client.get(url)
        # Should redirect to login because of @login_required
        self.assertEqual(response.status_code, 302)