from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
import random
from tasks.models import Project, Task, Notification, Member

# Read the URLs for NASA images
imageurls = open("static/nasa_imageurls").readlines()

def randomimg():
    return { 
            'image': random.choice(imageurls).strip()
    }


@require_GET
def demo(request):
    return render(request,'htmx/demo.html', randomimg())

@require_GET
def demo_bootstrap(request):
    return render(request,'htmx/demo_bootstrap.html', {})


# POST request example
@require_POST
def answer(request):
    try:
        value = int(request.POST['value'])
        func = request.POST['function']
        if func == "square":
            return render(request, "htmx/partials/answer.html", {'answer': value*value })
        else:
            return render(request, "htmx/partials/answer.html", {'answer': value*value*value })
    except:
        return render(request, "htmx/partials/answer.html",{'answer': "Invalid"})
    

@require_POST
def answer1(request):
    try:
        value = int(request.POST['value1'])
        func = request.POST['function1']
        if func == "square":
            return render(request, "htmx/partials/answer.html", {'answer': value*value })
        else:
            return render(request, "htmx/partials/answer.html", {'answer': value*value*value })
    except:
        return render(request, "htmx/partials/answer.html",{'answer': "Invalid"})

@require_GET
def oneimage(request):
    return render(request, 'htmx/partials/image.html', randomimg())

@require_GET
def example1(request):
    return render(request, 'htmx/example1.html', {})

@require_GET
def example2(request):
    return render(request, 'htmx/example2.html', {})

@require_GET
def example3(request):
    return render(request, 'htmx/example3.html', randomimg())

@require_GET
def example4(request):
    return render(request, 'htmx/example4.html', {
        'projects': Project.objects.all()
    })

@require_POST
def tasks4project(request):
    try:
        id = int(request.POST['id'])
        tasks = Task.objects.filter(project__id=id)
        return render(request, "htmx/partials/tasks.html", {
            'tasks': tasks            
        })
    except:
        return render(request, "htmx/partials/tasks.html", {
            'tasks': []             
        })
    
@require_GET
def member4task(request, id):
    try:
        # name = int(request.POST['name'])
        task = Task.objects.get(id=id)
        return render(request, "htmx/partials/member.html", {
            'member': task.assignee          
        })
    except:
        return render(request, "htmx/partials/member.html", {
            'member': []             
        })


@require_GET
def jsdemo(request):
    return render(request, "htmx/jsdemo.html", {})


@require_POST
def jsresponse(request):
    times = request.POST['response']
    responses = times.split(" ")
    previous = int(responses[0])
    responses.pop(0)
    answer = "Server received: "
    for response in responses:
        values = response.split(':')
        button = values[0]
        latency = (int(values[1]) - previous)/1000
        previous = int(values[1])
        answer = f"{answer} Button {button} after a latency of {latency} seconds. "
    return render(request, "htmx/partials/times.html",{
        'answer': answer
    }) 

@require_GET
def assignment(request):
    return render(request, "htmx/assignment.html", {})

@require_GET
def assignment_search(request):
    member_id = request.GET.get("member_id", "").strip()
    search_type = request.GET.get("type", "notifications").lower()

    member = Member.objects.filter(username=member_id).first()

    if not member:
        message = f"Team member with the name {member_id} does not exist."
        results = []
    else:
        results = list(
            member.notification_set.all()
            if search_type == "notifications"
            else member.task_set.all()
        )
        message = (
            f"There are no {search_type} for member {member_id}"
            if not results
            else f"{search_type.capitalize()} for team member {member_id} are as follows"
        )

    return render(request, "htmx/partials/assignment_results.html", {
        "results": results,
        "message": message,
        "search_type": search_type,
    })