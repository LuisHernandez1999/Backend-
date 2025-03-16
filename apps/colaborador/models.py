from django.db import models
from django.core.exceptions import ValidationError
import re


def validar_nome(value):
    if not re.match("^[A-Za-záéíóúÁÉÍÓÚàáãâêôûçÇ ]+$", value):
        raise ValidationError('formato errado')
    
def validar_pa(value):
    if value not in ["1", "2", "3", "4"]:
        raise ValidationError('numero de PA errado')

def validar_colaborador(value):
    if value not in ["Motorista", "Coletor", "Operador"]:
        raise ValidationError('tipo de colaborador errado ')
    
class Colaborador(models.Model):
    MOTORISTA = "Motorista"
    COLETOR = "Coletor"
    OPERADOR = "Operador"

    PA = ["1", "2", "3", "4"]  
    TURNOS = ["Matutino", "Vespertino", "Noturno"]  
    
    nome = models.CharField(max_length=255, validators=[validar_nome])
    matricula = models.CharField(max_length=50)
    pa = models.CharField(max_length=10, choices=[(x, x) for x in PA], validators=[validar_pa])
    turno = models.CharField(max_length=20, choices=[(y, y) for y in TURNOS])  
    tipo = models.CharField(max_length=20, choices=[
        (MOTORISTA, "Motorista"),
        (COLETOR, "Coletor"),
        (OPERADOR, "Operador")
    ], validators=[validar_colaborador])

    def __str__(self):
        return self.nome
