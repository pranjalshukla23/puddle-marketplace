from django.shortcuts import render, redirect
from items.models import Category, Item
from . forms import SignupForm

# Create your views here.

def index(request):
    # get items from db which are not sold
    items = Item.objects.filter(is_sold = False)[0: 6]
    # get all the categories from db
    categories = Category.objects.all()
    # render a template
    return render(request, 'core/index.html', {
        "categories": categories,
        "items": items
    })

def contact(request):
    # render a template
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == "POST":
        # create an instance of form with user provided data
        form = SignupForm(request.POST)
        
        if form.is_valid():
            # save and commit the form
            form.save()
            # redirect to a specific url
            return redirect("/login/")
    else:
        # create an empty instance of form
        form = SignupForm()
    
    # render a specific template
    return render(request, "core/signup.html", {
        "form": form
    })