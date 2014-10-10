from django import forms
from django.forms import ModelForm
from base.models import SalesPageContent

class TrainerIDForm(forms.Form):
    trainer_id = forms.CharField(max_length=5)
    program_name = forms.CharField(max_length=40)

class SalesPageForm(ModelForm):
    class Meta:
        model = SalesPageContent
        fields = ['name', 'url_slug', 'video_html', 
                  'program_title', 'program_introduction', 'social_proof_header_html',
                  'trainer_note', 'last_ditch_1', 'last_ditch_2',
                  'testimonial_1_text', 'testimonial_1_name', 
                  'testimonial_2_text', 'testimonial_2_name', 
                  'testimonial_3_text', 'testimonial_3_name']

