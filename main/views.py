from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProjectForm, MileStoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Project, Milestone, Notification


# landing page 
def landing_page(request): 
    if request.user.is_authenticated: 
        return redirect('home')
    
    return render(request, 'main/landing_page.html')

# home page 
@login_required(login_url="/login")
def home(request):
    projects = Project.objects.all().order_by('-updated_at')  # most recently updated posts to the top (chronological order feed)
    
    user_collabs= Notification.objects.filter(
        sender = request.user, 
        notification_type = 'collaborate'
    ).values_list('project_id', flat=True)
    
    if request.method == "POST":
        project_id = request.POST.get("project-id")
        content = request.POST.get("content")
        project = Project.objects.filter(id=project_id).first()
       
        # deletion
        if project and project.author == request.user: 
            project.delete()
            return redirect('/home')

      
    return render(request, 'main/home.html', {
        "projects":projects, 
        "user_collabs": user_collabs})

# celebration wall
@login_required(login_url="/login")
def celebration_wall(request): 
    projects = Project.objects.all().order_by('-updated_at')  # most recently updated posts to the top (chronological order feed)
    
    # get project ids the user has already congratulated (to prevent spam)
    user_celebrations = Notification.objects.filter(
        sender=request.user, 
        notification_type = 'celebrate'

    ).values_list('project_id', flat=True)
       

    return render(request, 'main/celebration_wall.html', {
        "projects":projects, 
        "user_celebrations": user_celebrations})



# registration
def sign_up(request): 
    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        # make a new user 
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('/home')

    else: 
        form = RegisterForm() 
    return render(request, 'registration/sign_up.html', {"form": form })


# log out
def logOut(request): 
    logout(request)
    return redirect("/login")

# login
@login_required(login_url="/login")
def create_project(request): 
    if request.method == 'POST': 
        form = ProjectForm(request.POST)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else: 
        form = ProjectForm() 
    
    return render(request, 'main/create_project.html', {"form": form })


# update existing project 

@login_required(login_url="/login")
def update_project(request, pk): 
    project = get_object_or_404(Project, pk=pk)
    # Ensure only the author can edit
    if project.author != request.user:
        return redirect('home')

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST":
    
        if "add-milestone" in request.POST:
            content = request.POST.get("content")
            if content:
                Milestone.objects.create(
                    project=project,
                    author=request.user,
                    content=content
                )
                project.save()

        #check if main project form needs saving
        if form.is_valid():
            form.save()
            # If they just added a milestone keep them on the edit page
            if "add-milestone" in request.POST:
                return redirect('update_project', pk=project.pk)
            
            return redirect("/home")

    return render(request, 'main/edit_project.html', {"form": form, "project": project})


# send a celebration notification 
@login_required(login_url="/login")
def send_celebration_notification(request, project_id): 
    project = get_object_or_404(Project, id=project_id) 
    author = project.author 

    # create notification if user is not author and this notification hasn't been sent yet
    if author != request.user: 
        already_sent  =Notification.objects.filter(
            sender=request.user, 
            project = project, 
            notification_type = 'celebrate'

        ).exists()
    
    if not already_sent: 
        Notification.objects.create(
            recipient= author, 
            sender = request.user, 
            project = project, 
            notification_type = 'celebrate'
        )
    return redirect('celebration_wall')


# send a collaboration request
@login_required(login_url="/login")
def send_collaboration_request(request, project_id): 
    project = get_object_or_404(Project, id=project_id)
    author = project.author

    # create the notification if the user is not the author + notification hasn't been sent yet
    if author != request.user: 
        already_sent = Notification.objects.filter(
            sender= request.user , 
            project = project, 
            notification_type = 'collaborate'
        ).exists()
 
    if not already_sent: 
        Notification.objects.create(
            recipient = author, 
            sender = request.user, 
            project = project, 
            notification_type = 'collaborate'
        )

    
    return redirect("home")


# view your notifications
@login_required(login_url="/login")
def notifications_view(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    
    #update the bell icon
    notifications.filter(is_read=False).update(is_read=True)

    # notification deletion
    if request.method == 'POST':
        notification_id = request.POST.get("notification-id")
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        
        notification.delete()
        return redirect('notifications') 

    return render(request, 'main/notifications.html', {'notifications': notifications})


@login_required(login_url="/login")
def project_details(request, pk): 
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'main/view_project.html',{"project": project})