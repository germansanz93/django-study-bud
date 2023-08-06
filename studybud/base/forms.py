from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #Indicamos que queremos un campo por cada valor (solo por el momento)