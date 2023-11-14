from django import forms
from .models import Person

class DateInput(forms.DateInput):
    input_type = 'date'

class PersonForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput(format='%m/%d/%Y'))

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'middle_name', 'birthdate', 'sex']