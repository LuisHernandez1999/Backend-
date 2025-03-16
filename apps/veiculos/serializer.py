from rest_framework import serializers
from .models import Veiculo


class SerializerVeiculo(serializers.ModelSerializer):
    class meta:
        model = Veiculo
        field = ["placa","tipo","prefixo","status"]
    