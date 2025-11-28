from django import forms
from .models import Viaje,Fuentes

class formviaje(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        
        labels = {
            'fecha': 'fecha del viaje',
            'inversion': 'inversion en pesos',
            }
        widgets = {
            'fecha': forms.DateInput(
              attrs={
                'class': 'form-control',
                'type': 'date',
                },
            format='%Y-%m-%d'
            ),
            
        'inversion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
class formfuente(forms.ModelForm):
    class Meta:
        model = Fuentes
        fields = ['fuente','invertido']

        labels = {
            'fuente': 'Fuente de inversion ',
            'inversion': 'inversion en pesos',
            }
        widgets = {
    'fuente': forms.TextInput(attrs={
        'class': 'form-control',
        
    }),
    'invertido': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': '0.00'
    })
}