from django import forms
from .models import Tweet, Relationship, images

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={"class":"form-control", "id":"textarea-post-form" , "rows":"3"})
        }
        labels = {
            'content': ""
        }

class LikeForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['likes']


class imagesForm(forms.ModelForm):
    class Meta:
        model = images
        fields = ['profile_image']
        labels = {
            'profile_image': ''
        }