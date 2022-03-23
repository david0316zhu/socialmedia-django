from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Relationship
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been successfully created!') 
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if update_form.is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()
            messages.success(request, f'Account information has been updated!') 
            return redirect('profile')

    else:
        update_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    profile = Profile.objects.get(user=request.user)
    count = profile.get_num_friends()
    friends = profile.get_friends()

    context = {
        'update_form': update_form,
        'profile_form': profile_form,
        'friends': friends,
        'count': count
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def invite_received(request):
    profile = Profile.objects.get(user=request.user)
    query = Relationship.objects.request_received(profile)
    result = list(map(lambda x: x.sender, query))
    is_null = False
    if len(result) == 0:
        is_null = True
    context = {
        "query": result,
        "is_null": is_null
    }
    return render(request, 'users/invites.html', context)

@login_required
def accept_request(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=user)
        try:
            relation_x = Relationship.objects.get(sender=receiver, receiver=sender, status="send")
            relation_x.delete()
        except ObjectDoesNotExist:
            pass

        
        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relation.status =="send":
            relation.status = "accepted"
            relation.save()

        return redirect('home')
    return redirect('home')

@login_required
def reject_request(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=user)
        relation = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relation.delete()

        return redirect('home')
    return redirect('home')


@login_required
def removal(request):
    if request.method == "POST":
        rec = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=rec)
        
        relation = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        relation.delete()
        return redirect('home')
    return redirect('home')

@login_required
def friend_request(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect('home')
    return redirect('home')