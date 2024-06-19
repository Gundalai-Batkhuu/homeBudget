from django.shortcuts import render


def index(request):
    context = {
        "greeting": "Hello, world!",
    }
    return render(request, "transactions/index.html", context)
