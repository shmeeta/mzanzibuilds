from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    
    STAGE_CHOICES = [
        ('idea', 'Idea/Concept'), 
        ('planning', 'Planning/Research'), 
        ('in_progress', 'Development/In Progress'),
        ('testing', 'Testing/QA'), 
        ('Completed', 'Completed/Deployed'),

    ]
    author = models.ForeignKey(User,on_delete=models.CASCADE)  # if user is deleted, post is also deleted
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    stage = models.CharField(
        max_length=20, 
        choices=STAGE_CHOICES,
        default='idea'
    )
    support_required = models.CharField(max_length=400, default="None")

    def __str__(self):
        return self.title + "\n" + self.description
    

class Milestone(models.Model): 
    project= models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return  f"{self.project.title} - {self.content[:20]}"
    

class Notification(models.Model): 

    TYPES = [
        ('celebrate', 'Celebration'),
        ('collaborate', 'Collaboration'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications' )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=TYPES)
    created_at= models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    @property
    def unread_exists(self): 
        return Notification.objects.filter(recipient=self.recipient, is_read=False).exists()

    def __str__(self):
        return f"{self.notification_type} from {self.sender.username}"


