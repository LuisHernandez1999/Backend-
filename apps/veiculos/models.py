from django.db import models
from django.core.exceptions import ValidationError
import re

from django.core.exceptions import ValidationError
import re

def validar_placa(value):
    padrao_novo = r"^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$"  
    padrao_antigo = r"^[A-Z]{3}-[0-9]{4}$"  

    if not re.match(padrao_novo, value) and not re.match(padrao_antigo, value):
        raise ValidationError('Formato de placa inválido. Use "AAA-1234" ou "AAA1B23".')

def validar_tipo(value,):
    if value not in ["Baú","Seletolux","Basculante"]:
        raise ValidationError("tipo de veiculo nao existente ")

def validar_prefixo(value, tipo_veiculo):
    if tipo_veiculo == "Baú" and value != "BAÚ":
        raise ValidationError("prefixo errado para o tipo de veículo ")
    if tipo_veiculo == "Seletolux" and value != "SL":
        raise ValidationError("prefixo errado para o tipo de veículo ")
    if tipo_veiculo == "Basculante" and value != "BS":
        raise ValidationError("prefixo errado para o tipo de veículo ")

def validar_status(value):
    if value not in ["Ativo", "Inativo"]:
        raise ValidationError("O status deve ser ativo ou inativo.")

def validar_motivo_inatividade(value, status):
    if status == "Inativo":
        if value not in ["Em manutenção", "Na garagem"]:
            raise ValidationError("motivo nao existe. Deve ser em manutenção ou na garagem.")

class Veiculo(models.Model):
    TIPO = ["Baú", "Seletolux", "Basculante"]
    PREFIXO = ["BS", "BAÚ", "SL"]
    STATUS = ["Ativo", "Inativo"]
    MOTIVO_INATIVIDADE = ["Em manutenção", "Na garagem"]

    placa = models.CharField(max_length=8, validators=[validar_placa])
    tipo = models.CharField(max_length=50, choices=[(y, y) for y in TIPO])
    prefixo = models.CharField(max_length=50, choices=[(x, x) for x in PREFIXO])
    status = models.CharField(max_length=50, choices=[(w, w) for w in STATUS], validators=[validar_status])
    motivo_inatividade = models.CharField(
        max_length=10,
        choices=[(m, m) for m in MOTIVO_INATIVIDADE],
    )

    def __str__(self):
        return self.placa

    def clean(self):
        validar_prefixo(self.prefixo, self.tipo)
        if self.status == "Inativo" and not self.motivo_inatividade:
            raise ValidationError("Motivo de inatividade é obrigatório quando o status é 'Inativo'.")
        if self.status == "Inativo":
            validar_motivo_inatividade(self.motivo_inatividade, self.status)
