from django import forms 
  
# iterable 
GEEKS_CHOICES =( 
    ("1", "One"), 
    ("2", "Two"), 
    ("3", "Three"), 
    ("4", "Four"), 
    ("5", "Five"),  
) 
  
# creating a form  
class GeeksForm(forms.Form):
    geeks_field = forms.ChoiceField(choices = GEEKS_CHOICES, widget=forms.Select(attrs={ "id": "button_Choice"}))#'onClick': 'load_data();'