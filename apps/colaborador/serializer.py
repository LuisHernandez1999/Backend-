from rest_framework import serializers
from .models import Colaborador

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['nome', 'matricula', 'pa', 'turno', 'tipo']