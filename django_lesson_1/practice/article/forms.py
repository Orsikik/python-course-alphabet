from django import forms
from article.models import Article, Comments, CommentsOnComments



class ArticleForm(forms.ModelForm):
    # title = forms.CharField(required=True)
    author = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = ('title', 'description')
        labels = {
            'title': 'Article name'
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('profile', 'email', 'text', 'article', )

class ComOnComForm(forms.ModelForm):

    class Meta:
        model = CommentsOnComments
        fields = ('article', 'profile', 'parent_comment', 'comment')