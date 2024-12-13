from django import forms
from .models import GeneticTest


class GeneticTestForm(forms.ModelForm):
   class Meta:
       model = GeneticTest
       fields = ['animal_name', 'species', 'test_date', 'milk_yield', 'health_status']
