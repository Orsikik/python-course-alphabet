from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import ProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class ProfileDetailView(UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    form_class = ProfileForm
    context_object_name = 'profile'          # обьявляем имя обьекта через которое будем обращатся в шаблонах
    pk_url_kwarg = 'pk'                      # обьявляем имя через которое передаем значение в юрл
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Created user
        created_user = form.save()
        # Create profile
        profile = Profile.objects.create(user=created_user)
        # Authentificate User
        auth_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1')
        )
        login(self.request, auth_user)
        return redirect('profile', profile.id)


## Code for social networks auth

# Create your views here.
def login(request):
    return render(request, 'login.html')
@login_required
def home(request):
    return render(request, 'home.html')