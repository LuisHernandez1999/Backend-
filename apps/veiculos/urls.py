from django.urls import path
from .views import (
    criar_veiculo,
    deletar_veiculo,
    editar_veiculo,
    quantidade_de_veiculos,
    quantidade_de_veiculos_inativos,
    quantidade_de_veiculos_ativos,
    retorna_detalhes_veiculos,
)

urlpatterns = [
    path("criar/", criar_veiculo, name="criar_veiculo"),
    path("deletar/<str:placa>/", deletar_veiculo, name="deletar_veiculo"),
    path("editar/<str:placa>/", editar_veiculo, name="editar_veiculo"),
    path("quantidade/", quantidade_de_veiculos, name="quantidade_de_veiculos"),
    path("quantidade/inativos/", quantidade_de_veiculos_inativos, name="quantidade_de_veiculos_inativos"),
    path("quantidade/ativos/", quantidade_de_veiculos_ativos, name="quantidade_de_veiculos_ativos"),
    path("detalhes/", retorna_detalhes_veiculos, name="retorna_detalhes_veiculos"),
]
