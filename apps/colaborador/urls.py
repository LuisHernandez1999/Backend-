from django.urls import path
from .views import editar_colaborador, criar_colaborador, retornar_dados_importantes,retorna_detalhes_colaboradores,quantidade_de_colaboradores,deletar_colaborador,colaboradores_por_turno

urlpatterns = [
    path('api/criar/', criar_colaborador, name='criar_colaborador'),
    path('api/deletar/<str:matricula>/', deletar_colaborador, name='deletar_colaborador'),
    path('api/editar/<str:matricula>/', editar_colaborador, name='editar_colaborador'),
    path('api/dados/<str:matricula>/', retornar_dados_importantes, name='retornar_dados_importantes'),
    path('api/detalhes/', retorna_detalhes_colaboradores, name='retorna_detalhes_colaboradores'),
    path('api/quantidade/', quantidade_de_colaboradores, name='quantidade_de_colaboradores'),
    path('api/colaboradores/turno/',colaboradores_por_turno, name= 'colaboradores_por_turno')
]
