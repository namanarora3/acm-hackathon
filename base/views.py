from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Location,Category,Tasks, UserData
from .forms import TaskImageForm,ApproveForm,TaskForm
from datetime import datetime
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

def loginPage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exist')

        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"incorrect password")
        
    return render(request,"base/login_registration.html")

def logoutPage(request):

    logout(request)
    return redirect("home")

@login_required(login_url='loginPage')
def home(request):
    # try:
    #     # print(request.user.coins.first().coins)
    # except ObjectDoesNotExist:
    #     print("There is no restaurant here.")

    q=request.GET.get('q') if request.GET.get('q') != None else ''
    if request.user.is_staff:
        tasks = Tasks.objects.filter(
            Q(location__name__icontains = q) |
            Q(category__name__icontains = q)
        ).annotate(null_nullcompleted = Count("completed")).order_by('-null_nullcompleted','approved','created')
        # users = User.objects.annotate(count = Count("tasks"))
        # for user in users:
        #     print(user.username,user.count)
    else:
        tasks = request.user.tasks_set.filter(
            Q(location__name__icontains = q) |
            Q(category__name__icontains = q)
        ).annotate(null_nullcompleted = Count("completed")).order_by('null_nullcompleted','-approved','created')
    # print(tasks)
    location = Location.objects.all()
    category = Category.objects.all()
    context = {'tasks':tasks,'locations':location, "categories":category}
    return render(request,"base/home.html",context)

@login_required(login_url='loginPage')
def task_image(request,pk):
# room=Room.objects.get(id=pk)
    task=Tasks.objects.get(id=pk)
    if(request.user == task.assigned):
        form=TaskImageForm(instance=task)
        if request.method == "POST":
            form = TaskImageForm(request.POST,request.FILES,instance=task)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.completed = datetime.now()
                temp.save()
                # messages.SUCCESS(request,"Successfully uploaded")
                return redirect('home')
        context = {"form":form,"task":task}
        return render(request,'base/task_image.html',context)
    else:
        return HttpResponse("you arent allowed here")
    


@login_required(login_url='loginPage')
def task_approve(request,pk):
# room=Room.objects.get(id=pk)
    task=Tasks.objects.get(id=pk)
    # userd = UserData.objects.get(user = task.assigned)
    if(request.user.is_staff):
        form=ApproveForm(instance=task)
        if request.method == "POST":
            done = request.POST.get('approved', False)
            form = ApproveForm(request.POST, instance=task)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.approved = bool(done)
                temp.save()
                print(userd.coins, task.coins)
                userd.coins = userd.coins + task.coins
                userd.save()
                return redirect("home")
        context = {"form":form,"task":task}
        return render(request,'base/task_approve.html',context)
    else:
        return HttpResponse("login as ADMIN user")
    

@login_required(login_url='loginPage')
def task_form(request):
# room=Room.objects.get(id=pk)
    category=Category.objects.all()
    location=Location.objects.all()
    tuser=User.objects.all()
    if(request.user.is_staff):
        form=TaskForm()
        if request.method == "POST":
            category_name = request.POST.get('category')
            category_n,created = Category.objects.get_or_create(name=category_name)
            location_name = request.POST.get('location')
            location_n,created = Location.objects.get_or_create(name=location_name)
            user_name = request.POST.get('assigned')
            user_n = User.objects.get(username = user_name)
            name_n = request.POST.get('name')
            Tasks.objects.create(
                name = name_n,
                assigned = user_n,
                location = location_n,
                category = category_n,
                coins = request.POST.get('coins')
            )
            # form = TaskForm(request.POST)
            # if form.is_valid():
            #     temp = form.save(commit=False)
            #     # temp.approved_time = datetime.now()
            #     temp.save()
            return redirect("home")
        context = {"form":form,"categories":category,"locations":location,"tusers":tuser}
        return render(request,'base/task_form.html',context)
    else:
        return HttpResponse("Login as ADMIN user")