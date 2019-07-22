from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article, Comments, CommentsOnComments
from .forms import ArticleForm, CommentForm, ComOnComForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.urls import reverse
from account.models import Profile
from article.mixins import FormMessageMixin
from django.views.generic.edit import ModelFormMixin
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
# Create your views here.
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages


class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['page_title'] = 'All articles'
        return context

    def get_queryset(self):
        return Article.objects.all()[:2]


# def index(request):
#     articles = Article.objects.all()
#     return render(request, 'index.html', {'articles': articles})

class ArticleCreateView(FormMessageMixin, CreateView):
    model = Article
    template_name = 'article/create.html'
    form_class = ArticleForm
    form_valid_message = 'Article created successfully!'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super(ArticleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail', args=(self.object.id,))


# def create(request):
#     form = ArticleForm()
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             s_form = form.save()
#         return redirect('detail', s_form.id)
#     return render(request, 'article/create.html', {'form': form})


class ArticleDetailViev(ModelFormMixin, DetailView):
    model = Article
    template_name = 'article/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    form_class = CommentForm
    post_comments_class = CommentForm
    post_com_on_com_class = ComOnComForm

    def get_context_data(self, **kwargs):
        article = self.get_object()
        context = super(ArticleDetailViev, self).get_context_data()
        comments = Comments.objects.filter(article=article).order_by('created')
        # PAGINATION
        paginator = Paginator(comments, 1)
        request = self.request
        page = request.GET.get('page', 1)
        p_comments = paginator.get_page(page)
        #Context data
        context['p_comments'] = p_comments
        context['comments'] = Comments.objects.filter(article=article)
        context['nested_comments'] = CommentsOnComments.objects.filter(article=article)
        # context['form'] = self.get_form()
        return context

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     comment = form.save()
    #     return redirect('detail', comment.article.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_data = request.POST or None
        comment_form = self.post_comments_class(post_data, prefix='comment')
        com_on_com_form = self.post_com_on_com_class(post_data, prefix='com_on_com')
        context = self.get_context_data(comment_form=comment_form, com_on_com_form=com_on_com_form)
        print('Before form validation')
        print(comment_form)
        # print(com_on_com_form)
        print(comment_form.errors)
        if comment_form.is_valid():
            print('In condition block')
            self.form_save(comment_form)
        if com_on_com_form.is_valid():
            self.form_save(com_on_com_form)

        return self.render_to_response(context)

    def form_valid(self, form):
        comment = form.save()
        return redirect('detail', comment.article.id)

    def form_save(self, form):
        obj = form.save()
        messages.success(self.request, "{} saved successfully".format(obj))
        return obj



class ArticleDetailViewComForm(FormView):
    form_class = ComOnComForm
    success_url = '/'
    template_name = 'article/detail.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ArticleDetailViewComForm, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailViewComForm, self).get_context_data(**kwargs)
        context['article_detail_viev_in_action'] = False
        return context



# def detail(request, article_id):
#     article = Article.objects.get(id=article_id)
#     return render(request, 'article/detail.html', {'article': article})


class ArticleUpdateView(FormMessageMixin, UpdateView):
    model = Article
    template_name = 'article/update.html'
    form_class = ArticleForm
    pk_url_kwarg = 'article_id'
    form_valid_message = 'Updated successfully!'

    def get_success_url(self):
        return reverse('detail', args=(self.object.id,))


class ArticleDeleteView(DeleteView):
    model = Article
    pk_url_kwarg = 'article_id'
    success_url = '/'
    template_name = 'article/confirm_delete.html'
    context_object_name = 'article'


