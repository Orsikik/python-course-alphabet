"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from article.views import IndexView, ArticleCreateView, ArticleDetailViev, ArticleUpdateView, ArticleDeleteView, ArticleDetailViewComForm
from account.views import ProfileDetailView, SignUp, login, home
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    # Article
    path('', IndexView.as_view(), name='index'),
    path('article/create', ArticleCreateView.as_view(), name='create'),
    path('article/<int:article_id>', ArticleDetailViev.as_view(), name='detail'),
    # path('article/<int:article_id>/new_comment', ArticleDetailViewComForm.as_view(), name='new_comment'),
    path('article/update/<int:article_id>', ArticleUpdateView.as_view(), name='update'),
    path('article/delete/<int:article_id>', ArticleDeleteView.as_view(), name='delete'),


    #Account
    # path('account/profile/<int:profile_id>', ProfileDetailView.as_view(), name='profile'),
    path('account/profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('account/profile/<str:slug>', ProfileDetailView.as_view(), name='profile'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/signup', SignUp.as_view(), name='signup'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #Social network auth
    path("login/", login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("", home, name="home"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
