from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Milestone, Notification

class MainAppTests(TestCase):
    def setUp(self):
        # Create users
        self.user_a = User.objects.create_user(username='DevUserA', password='password123')
        self.user_b =User.objects.create_user(username='DevUserB', password='password123')
        
        # Create project for A
        self.project = Project.objects.create(
            author= self.user_a,
            title= "Initial Title",
            description= "Initial Description",
            stage= "idea"
        )

    def test_update_project_and_add_milestone_simultaneously(self):
        """Tests the bug fix: changing title and adding milestone in one click"""
        self.client.login(username='DevUserA', password='password123')
        
        url = reverse('update_project', kwargs={'pk': self.project.pk})
        
        #Send request that tries to change the title + add a milestone
        response= self.client.post(url, {
            'title': 'Updated Project Title' ,
            'description': 'Initial Description',
            'stage': 'planning' ,
            'support_required': 'Mentorship' ,
            'add-milestone': 'true',  # The trigger in your view
            'content': 'First milestone reached' # The milestone text
        })

        # rerfresh from db 
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project Title')
        self.assertEqual(self.project.milestones.count(), 1)
        self.assertEqual(self.project.milestones.first().content, 'First milestone reached!')
        self.assertRedirects(response, url)

    def test_notification_unread_property(self): # test @ property unread_exists in notification model logic
        notification = Notification.objects.create(
            recipient=self.user_a,
            sender=self.user_b,
            project=self.project,
            notification_type='celebrate'
        )
        # check if the property works
        self.assertTrue(notification.unread_exists)
        
        # mark as read + check again
        notification.is_read = True
        notification.save()
        
        #shouold be false for no other unread notifications
        self.assertFalse(notification.unread_exists)

    def test_unauthorized_edit_protection(self):
        # non author shouldnt be able to edit another author's project
        self.client.login(username='DevUserB', password='password123')
        
        url = reverse('update_project', kwargs={'pk': self.project.pk})
        response = self.client.post(url, {'title': 'Hacked Title'})
        
        #refresh from db
        self.project.refresh_from_db()
        
        #title shouldnt have changed
        self.assertEqual(self.project.title, "Initial Title")
        # ensure redirect
        self.assertRedirects(response, reverse('home'))