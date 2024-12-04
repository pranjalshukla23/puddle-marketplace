from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm

def items(request):
    # get the query from the request
    query = request.GET.get('query', '')
    # get the category mentioned in the request 
    category_id = request.GET.get('category', 0)
    # get all the categories
    categories = Category.objects.all()
    # get the items from db which are not sold
    items = Item.objects.filter(is_sold=False)
    
    if category_id:
        # get the items that belong to a specific category
        items = items.filter(category_id=category_id)
    
    if query:
        # get the items where the name or description contains the word mentioned in the query
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    return render(request, 'items/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

# Create your views here.
def detail(request, pk):
    # get records from Item model using primary key
    item = get_object_or_404(Item, pk=pk)
    # get items that belong to the same category and are not sold
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
     # render a template
    return render(request, 'items/detail.html', {
        "item": item,
        "related_items": related_items
    })
    
@login_required
def new(request):
    if request.method == "POST":
        # create an instance of form with user provided data
        form = NewItemForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            # save the item but don't commit in database
            item = form.save(commit=False)
            item.created_by = request.user
            # save and commit the item
            item.save()
            
            # redirect to a specific url
            return redirect("item:detail", pk=item.id)
    
    else: 
        # create an empty instance of form
        form = NewItemForm()
    # render a template
    return render(request, 'items/form.html', {
        'form': form,
        'title': 'New Item'
    })   

@login_required
def edit(request, pk):
    # get records from Item model which matches the primary key and are created by the logged in user 
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == "POST":
        # create an instance of form with user provided data
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            # save the item in db
            item = form.save()
            
            # redirect to a specific url
            return redirect("item:detail", pk=item.id)
    
    else: 
        form = EditItemForm(instance=item)
    
    # render a template
    return render(request, 'items/form.html', {
        'form': form,
        'title': 'Edit Item'
    })  

@login_required  
def delete(request, pk):
    # get records from Item model which matches the primary key and are created by the logged in user 
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    # delete the item from db
    item.delete()
    # redirect to a specific url
    return redirect("dashboard:index")