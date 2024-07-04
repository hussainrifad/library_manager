from .models import UserInformation
from django import forms
from .constants import GENDER
from django.contrib.auth.models import User

class UserInformationForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    institution = forms.CharField(max_length=128)
    group = forms.CharField(max_length=32)
    grade = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER)
    country = forms.CharField(max_length=128)
    
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return password

    def save(self, commit=True):
        current_user = super().save(commit=False)
        current_user.set_password(self.cleaned_data.get('password'))

        if commit == True:
            current_user.save()
            birth_date = self.cleaned_data.get('birth_date')
            institution = self.cleaned_data.get('institution')
            group = self.cleaned_data.get('group')
            grade = self.cleaned_data.get('grade')
            gender = self.cleaned_data.get('gender')
            country = self.cleaned_data.get('country')

            UserInformation.objects.create(
                user=current_user,
                institution=institution,
                group=group,
                gender=gender,
                grade=grade,
                country=country,
                birth_date=birth_date
            )
        return current_user

class UserInformationUpdateForm(forms.ModelForm):
    institution = forms.CharField(max_length=128)
    group = forms.CharField(max_length=32)
    grade = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER)
    country = forms.CharField(max_length=128)

    class Meta:
        password = None
        model = User
        fields = fields = ['username','first_name', 'last_name', 'email']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        if self.instance:
            try:
                user_information = self.instance.information
            except User.information.DoesNotExist:
                user_information = None

            if user_information:
                    self.fields['institution'].initial = user_information.institution
                    self.fields['group'].initial = user_information.group
                    self.fields['grade'].initial = user_information.grade
                    self.fields['gender'].initial = user_information.gender
                    self.fields['country'].initial = user_information.country

    def save(self, commit=True):
        current_user = super().save(commit=False)
        if commit == True:
            current_user.save()

            user_information, created = UserInformation.objects.get_or_create(user=current_user)
            user_information.institution = self.cleaned_data.get('institution')
            user_information.group = self.cleaned_data.get('group')
            user_information.grade = self.cleaned_data.get('grade')
            user_information.gender = self.cleaned_data.get('gender')
            user_information.country = self.cleaned_data.get('country')

            user_information.save()
            
        return current_user

class DepositeForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=0, max_value=1000)
    class Meta:
        model = User
        fields = ['amount']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })