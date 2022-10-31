from django import forms
from django.forms import ModelForm
from ts_system.models import *

# Create your forms here.

# class ContactForm(forms.Form):
#     to_email = forms.EmailField(required=True)
#     subject = forms.CharField(required=True)
#     message = forms.CharField(widget=forms.Textarea, required=True)

class is_shipped_Form(ModelForm):
    class Meta:
        model = ts_data
        fields = ['IS_SHIPPED']

is_shipped_field = is_shipped_Form()

class UTIDs_Form(ModelForm):
    class Meta:
        model = ts_data
        fields = ['UTID']
utids_list = UTIDs_Form('UTID')

class Find_UTID_Form(forms.Form):
    OPTIONS = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )
    UTIDs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class UTIDs_swaping_Form(forms.ModelForm):
    class Meta:
        model = ts_data
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['UTID'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')