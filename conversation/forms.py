from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        # model to use for storing data
        model = ConversationMessage
        # fields to show and the order of fields
        fields = ('content',)
        # adding css to form fields
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }