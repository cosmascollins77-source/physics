from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser, TeacherProfile, StudentProfile, UserNotification, UserPreference
from .forms import UserRegistrationForm, ProfileEditForm, PreferencesForm


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('topics:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('topics:home')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile based on user type
            if user.user_type == 'student':
                StudentProfile.objects.create(user=user)
            elif user.user_type == 'teacher':
                TeacherProfile.objects.create(user=user)
            
            # Create user preferences
            UserPreference.objects.create(user=user)
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('topics:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """User profile page"""
    user = request.user
    
    # Get user-specific profile
    if hasattr(user, 'student_profile'):
        profile = user.student_profile
    elif hasattr(user, 'teacher_profile'):
        profile = user.teacher_profile
    else:
        profile = None
    
    # Get recent notifications
    notifications = UserNotification.objects.filter(user=user).order_by('-created_at')[:10]
    
    context = {
        'profile': profile,
        'notifications': notifications,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    user = request.user
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=user)
    
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def notifications(request):
    """User notifications"""
    user = request.user
    
    # Get all notifications
    notifications = UserNotification.objects.filter(user=user).order_by('-created_at')
    
    # Mark as read if requested
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = UserNotification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def preferences(request):
    """User preferences"""
    user = request.user
    
    try:
        preferences = user.preferences
    except UserPreference.DoesNotExist:
        preferences = UserPreference.objects.create(user=user)
    
    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated successfully!')
            return redirect('users:preferences')
    else:
        form = PreferencesForm(instance=preferences)
    
    return render(request, 'users/preferences.html', {'form': form})