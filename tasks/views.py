from django.shortcuts import render
from .models import Member

# Create your views here.
def listnotifications(request, username):
    member = Member.objects.filter(username=username).first()
    
    if member:
        notifications = member.notification_set.all()
    else:
        notifications = []
    
    return render(request, "tasks/listnotifications.html", {
        'username': username,
        'notifications': notifications,
        'member': member
    })