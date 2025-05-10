from django.shortcuts import render

def HomePage(request):
    logedusername = "Unknown user"
    if request.user.is_authenticated:
        logedusername = request.user.username
    return render(request, 'home.html', {'username': logedusername})