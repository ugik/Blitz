from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import datetime
import re

from base.models import Trainer, Blitz, BlitzInvitation
from workouts.models import WorkoutPlan

MACROS_CHOICES = (('DEFAULT', 'Default',), ('BULK', 'Bulk',), ('CUT', 'Cut',), ('BEAST', 'Beast',))
BLITZ_TYPE_CHOICES = (('GRP', 'Group',), ('IND', 'Individual',))

class LoginForm(forms.Form):

    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    user = forms.CharField(required=False)

    def clean_user(self):
        try:
            user = User.objects.get(email=self.cleaned_data.get('email', '').lower())
        except ObjectDoesNotExist:
            raise forms.ValidationError("This email address looks weird. Can you double check?")
        self.user = authenticate(username=user.username, password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError("The password you entered wasn't right. Give it another shot.")
        return self.user


class EmailRegisterForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput())

    def email(self):
        email = self.cleaned_data.get('email')

        if not re.match(r'[\w-]*$', email) :
            raise forms.ValidationError("Letters and numbers only, please.")

        return email


class ImageForm(forms.Form): 
    image = forms.FileField()

class NewTrainerForm(forms.Form):

    name =      forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    short_name  = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'yourname'}))
    email =     forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'render_value' : False}),max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'render_value' : False}),max_length=100)
    timezone  = forms.CharField(max_length=40)

    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')

        if not re.match(r'[\w-]*$', short_name) :
            raise forms.ValidationError("Letters and numbers only, please.")

        already_exists = Trainer.objects.filter(short_name__iexact=short_name)
        if already_exists:
            raise forms.ValidationError("Short name taken by %s" % already_exists[0].name)

        return short_name

    def clean_password1(self):
        data = self.cleaned_data['password1']
        if len(data) < 4:
            raise forms.ValidationError("Please make your password at least 4 characters long.")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email address is already registered.")
        return data

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("These passwords don't match. Try again, chief.")
        return self.cleaned_data

class SpotterProgramEditForm(forms.Form):
    edit_request = forms.CharField(widget=forms.Textarea())


class NewClientForm(forms.Form):

    name = forms.CharField(max_length=100, required=True)
    email =  forms.EmailField()
    invite = forms.CharField(widget=forms.Textarea(), required=False)
    signup_key = forms.CharField(max_length=10)

    price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'Charge $'}), required=False)
    workoutplan_id = forms.CharField(max_length=5, required=False)

    formulas = forms.ChoiceField(widget=forms.RadioSelect, choices=MACROS_CHOICES)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email address is already registered.")
        if BlitzInvitation.objects.filter(email=data).exists():
            raise forms.ValidationError("This email address is already invited.")
        return data

class BlitzSetupForm(forms.Form):

    title = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Program Name'})) 
    url_slug = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder': 'url'}))
    start_day = forms.DateField(initial=datetime.date.today,
                                widget=forms.DateInput(attrs= {'class': 'datepicker', 'id':'datepicker', 'placeholder':'Start Date'} ))
    charge = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'How much do you want to charge?'}))
    blitz_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BLITZ_TYPE_CHOICES, required=False)

    trainer = Trainer()
    formulas = forms.ChoiceField(widget=forms.RadioSelect, choices=MACROS_CHOICES)

    def __init__(self,*args,**kwargs):
        trainer = kwargs.pop("trainer")     # client is the parameter passed from views.py
        super(BlitzSetupForm, self).__init__(*args,**kwargs)
        if trainer:
            self.trainer = trainer

    def clean_url_slug(self):
        url_slug = self.cleaned_data.get('url_slug')

        if not re.match(r'[\w-]*$', url_slug) :
            raise forms.ValidationError("Letters and numbers only, please.")

        already_exists = Blitz.objects.filter(url_slug__iexact=url_slug, trainer=self.trainer)
        if already_exists:
            raise forms.ValidationError("This URL is already being used.")

        return url_slug

class SetPasswordForm(forms.Form):

    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)

    def clean_password1(self):
        data = self.cleaned_data['password1']
        if len(data) < 4:
            raise forms.ValidationError("Please make your password at least 8 characters.")
        return data

    def clean(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError("These passwords do not match. Give it another shot.")
        return self.cleaned_data

class ForgotPasswordForm(forms.Form):

    email = forms.CharField(max_length=100)

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data.get('email', '').lower())
        except ObjectDoesNotExist:
            raise forms.ValidationError("This email doesn't look right.")
        return self.cleaned_data['email']

class UploadForm(forms.Form): 
    document = forms.FileField()

class ClientCheckinForm(forms.Form): 
    front_image = forms.ImageField(required=False)
    side_image = forms.ImageField(required=False)
    weight = forms.IntegerField(min_value=0, max_value=500, required=False)

class TrainerUploadsForm(forms.Form): 
    headshot_image = forms.ImageField(required=False)
    logo_image = forms.ImageField(required=False)
    document = forms.FileField(required=False)

class SalesBlitzForm(forms.Form): 
    FEE_CHOICES = (('O', 'One-time',), ('R', 'Recurring',))

    picture = forms.ImageField(required=False)
    logo_picture = forms.ImageField(required=False)
    price_model = forms.ChoiceField(widget=forms.RadioSelect, choices=FEE_CHOICES)

class ClientSettingsForm(forms.Form): 
    picture = forms.ImageField()

# Feed comment
class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(), required=False)
    picture = forms.ImageField()

class Intro1Form(forms.Form): 
    UNITS_CHOICES = (('I', 'Imperial',), ('M', 'Metric',))

    age = forms.IntegerField(min_value=13, max_value=100)
    weight = forms.IntegerField(min_value=0, max_value=500)
    height_feet = forms.IntegerField(min_value=0, max_value=10)
    height_inches = forms.IntegerField(min_value=0, max_value=99)
    units = forms.ChoiceField(widget=forms.RadioSelect, choices=UNITS_CHOICES)
    gender = forms.CharField(max_length=1)

class MacrosForm(forms.Form): 

    formulas = forms.ChoiceField(widget=forms.RadioSelect, choices=MACROS_CHOICES)

class ProfileURLForm(forms.Form):
    picture = forms.ImageField()

class CreateAccountForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already registered.")
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 8:
            raise forms.ValidationError("Passwords must be at least 8 characters.")
        return data

class SubmitPaymentForm(forms.Form):

    card_uri = forms.CharField(max_length=100)

class SetMacrosForm(forms.Form):

    training_calories_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_protein_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_fat_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_carbs_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_calories_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_protein_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_fat_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_carbs_min = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))

    training_calories = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_protein = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_fat = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    training_carbs = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_calories = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_protein = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_fat = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))
    rest_carbs = forms.IntegerField(widget=forms.TextInput(attrs={'class':'span1', 'placeholder': '0'}))

