from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProjectForm, MileStoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Project, Milestone


# home page 
@login_required(login_url="/login")
def home(request):
    projects = Project.objects.all().order_by('-updated_at')  # most recently updated posts to the top (chronological order feed)
    if request.method == "POST":
        project_id = request.POST.get("project-id")
        content = request.POST.get("content")
        project = Project.objects.filter(id=project_id).first()
       
        # deletion
        if project and project.author == request.user: 
            project.delete()
            return redirect('/home')

      
    return render(request, 'main/home.html', {
        "projects":projects})


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
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST":
        # CHECK: Is the user trying to add a milestone?
        if "add-milestone" in request.POST:
            content = request.POST.get("content")
            if content:
                Milestone.objects.create(
                    project=project,
                    author=request.user,
                    content=content
                )
                # Redirect back to the same edit page to see the new update
                project.save()
                return redirect('update_project', pk=project.pk)

        # check if the user trying to save the whole project
        elif form.is_valid():
            form.save()
            return redirect("/home")

    return render(request, 'main/edit_project.html', {"form": form, "project": project})