from django import forms


class AddCommentForm(forms.Form):
    subject = forms.CharField(max_length=50, widget=forms.TextInput({'placeholder': 'Subject'}))
    content = forms.CharField(widget=forms.Textarea({'placeholder': 'Type Your Comment'}))
