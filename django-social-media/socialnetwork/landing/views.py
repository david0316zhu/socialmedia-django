from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from .models import Post
from users.models import Profile, Relationship
from django.contrib import messages





class PostListView(View):
    model = Post
    ordering = ['-date_posted']
    
    
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            friends = profile.get_friends()
            context = {
            'posts': Post.objects.all().order_by('-date_posted'),
            "friends": friends,
            "me": [request.user]
            }
        except:
            context = {}
        return render(request, 'landing/index.html', context)


class UserPostListView(LoginRequiredMixin, View):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    
    

    def get(self, request, *args, **kwargs):    
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user_posts = Post.objects.filter(user=user).order_by('-date_posted')
        profile = Profile.objects.get(user=request.user)
        friends = profile.get_friends()
        relation_r = Relationship.objects.filter(sender=profile)
        relation_s = Relationship.objects.filter(receiver=profile)
        relation_receiver = []
        relation_sender = []
        context = {'posts': user_posts}
        for item in relation_r:
            relation_receiver.append(item.receiver.user)
        for item in relation_s:
            relation_sender.append(item.sender.user)

        context["relation_receiver"] = relation_receiver
        context["relation_sender"] = relation_sender
        context['is_null'] = False
        if len(Profile.objects.get_all_profiles(request.user)) == 0:
            context['is_null'] = True

        
        if request.user == user:
            context["me"] = True
        else:
            context["me"] = False
            if user in friends:
                context["friend"] = True
                target = Profile.objects.get(user=user)
                context["target"] = target
            else:
                target = Profile.objects.get(user=user)
                context["target"] = target
                context["friend"] = False

        return render(request, 'landing/user_posts.html', context)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect('home')
#def home(request):
    #return render(request, 'landing/index.html')


@login_required
def search_user(request):
    if request.method=='POST':
        user_search = request.POST.get('user_search')
        context = {}
        if len(user_search) > 0:
            search_results = Profile.objects.filter(user__username__icontains=user_search)
            context["is_null"] = False
            context["results"] = search_results
            return render(request, 'landing/search.html', context)
        else:
            context["is_null"] = True
            return render(request, 'landing/search.html', context)

    return redirect('home')


