from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from conversation.models import Conversation
from items.models import Item
from .forms import ConversationMessageForm

# Create your views here.
@login_required
def new_conversation(request, item_pk):
    # get item from db which has the provided primary key
    item = get_object_or_404(Item, pk=item_pk)
    
    if item.created_at == request.user:
        # redirect to a specific url
        return redirect('dashboard:index')
    
    # get conversations that belong to this item and user from db 
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)
    
    if request.method == "POST":
        # create an instance of form with user provided data
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            # create an instance of conversation
            conversation = Conversation.objects.create(item=item)
            # add user to the conversation instance
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            # save and commit the conversation
            conversation.save()
            
            # save the form instance but do not commit it
            conversation_message = form.save(commit=False)
            # add convesation to form instance
            conversation_message.conversation = conversation
            # add user to form instance
            conversation_message.created_by = request.user
            # save and commit the form
            conversation_message.save()
            
            # redirect to specific url
            return redirect('item:detail', pk=item_pk) 
        
    else:
        # create an empty instance of form
        form = ConversationMessageForm()
            
    # render a template
    return render(request, 'conversations/new.html', {
        'form': form
    })
    
@login_required
def inbox(request):
    # get conversations that contains this user as the member from db 
    conversations = Conversation.objects.filter(members__in=[request.user.id])   
    
    # render a template
    return render(request, 'conversations/inbox.html', {
        'conversations': conversations
    })
    
@login_required
def detail(request, pk):
    # get conversations that contains this user as the member from db and which belong to this primary key
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    
    if request.method == "POST":
        # create an instance of form with user provided data
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            # save the form instance but do not commit it
            conversation_message = form.save(commit=False)
            # add convesation to form instance
            conversation_message.conversation = conversation
            # add user to form instance
            conversation_message.created_by = request.user
            # save and commit the form
            conversation_message.save()
            
            # save the conversation
            conversation.save()
            
            return redirect('conversation:detail', pk=pk)
    else:
        # create an empty instance of form
        form = ConversationMessageForm()
    
    # render a template
    return render(request, 'conversations/detail.html', {
        'conversation': conversation,
        'form': form
    })