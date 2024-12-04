from django.shortcuts import get_object_or_404, render
from items.models import Item
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    # get items from Item model which are created by the logged in user
    items = Item.objects.filter(created_by=request.user)
    # render a template
    return render(request,  'dashboard/index.html', {
        'items': items
    }) 
    

    