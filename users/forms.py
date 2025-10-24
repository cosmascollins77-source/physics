from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserPreference


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    school = forms.CharField(max_length=200, required=False)
    grade_level = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone_number', 'date_of_birth', 'school', 'grade_level', 
                 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.school = self.cleaned_data['school']
        user.grade_level = self.cleaned_data['grade_level']
        
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    """Profile editing form"""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                 'date_of_birth', 'school', 'grade_level', 'profile_picture', 'bio')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PreferencesForm(forms.ModelForm):
    """User preferences form"""
    class Meta:
        model = UserPreference
        fields = ('email_notifications', 'push_notifications', 'study_reminders', 
                 'achievement_notifications', 'weekly_progress_reports', 'dark_mode', 
                 'language', 'timezone')
        widgets = {
            'email_notifications': forms.CheckboxInput(),
            'push_notifications': forms.CheckboxInput(),
            'study_reminders': forms.CheckboxInput(),
            'achievement_notifications': forms.CheckboxInput(),
            'weekly_progress_reports': forms.CheckboxInput(),
            'dark_mode': forms.CheckboxInput(),
        }
