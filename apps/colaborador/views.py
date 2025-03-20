import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Colaborador

@csrf_exempt
@require_http_methods(["POST"])
def criar_colaborador(request):
    try:
        data = json.loads(request.body)  
        if Colaborador.objects.filter(matricula=data["matricula"]).exists():
            return JsonResponse({"erro": "matricula repetida."}, status=400)
        
        colaborador = Colaborador.objects.create(
            nome=data["nome"],
            matricula=data["matricula"],
            pa=data["pa"],
            turno=data["turno"],
            tipo=data["tipo"]
        )
        return JsonResponse({"mensagem": f"colaborador criado com sucesso: {colaborador.nome}"}, status=201)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
def retornar_dados_importantes(request,matricula):
    try:
        _ = request.method 
        if not matricula:
            return JsonResponse({"erro": "Matrícula não informada."}, status=400)
        colaboradores = Colaborador.objects.filter(matricula__icontains=matricula)
        if not colaboradores:
            return JsonResponse({"erro": f"nenhum colaborador encontrado com matrícula '{matricula}'"}, status=404)
        dados = [{"nome": c.nome, "matricula": c.matricula, "pa": c.pa, "turno": c.turno, "tipo": c.tipo} for c in colaboradores]
        return JsonResponse({"colaboradores": dados})
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["PUT"])
def editar_colaborador(request, matricula): 
    try:
        data = json.loads(request.body)
        colaborador = Colaborador.objects.get(matricula=matricula)  
        colaborador.nome = data["nome"]
        colaborador.pa = data["pa"]
        colaborador.turno = data["turno"]
        colaborador.tipo = data["tipo"]
        colaborador.save()
        return JsonResponse({"mensagem": f"colaborador {colaborador.nome} atualizado com sucesso"})
    except Colaborador.DoesNotExist:
        return JsonResponse({"erro": f"colaborador com matricula {matricula} nao encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def deletar_colaborador(request, matricula):
    try:
        _ = request.method 
        colaborador = Colaborador.objects.get(matricula=matricula)
        colaborador.delete()
        return JsonResponse({"mensagem": f"colaborador com matricula {matricula} deletado com sucesso."})
    except Colaborador.DoesNotExist:
        return JsonResponse({"erro": f"colaborador com matricula {matricula} não encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt 
@require_http_methods(["GET"])
def quantidade_de_colaboradores(request):
    try:
        _ = request.method 
        total = Colaborador.objects.count()
        return JsonResponse({"quantidade_de_colaboradores": total})
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt 
@require_http_methods(["GET"])
def retorna_detalhes_colaboradores(request):
    _ = request.method 
    try:
        colaboradores_query_set = Colaborador.objects.exclude(nome=None, matricula=None, pa=None, turno=None, tipo=None)
        colaboradores_data = list(colaboradores_query_set.values("nome", "matricula", "pa", "turno", "tipo"))
        return JsonResponse(colaboradores_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def colaboradores_por_turno(request):
    _ = request.method 
    try:
        colaboradores_query_set = Colaborador.objects.exclude(
            nome=None, matricula=None, pa=None, turno=None, tipo=None
        )
        noturnos = colaboradores_query_set.filter(turno="Noturno")
        vespertinos = colaboradores_query_set.filter(turno="Vespertino")
        matutinos = colaboradores_query_set.filter(turno="Matutino")
        quantidade_de_motoristas = colaboradores_query_set.filter(tipo="Motorista").count()
        quantidade_de_coletores = colaboradores_query_set.filter(tipo="Coletor").count()
        quantidade_de_operadores = colaboradores_query_set.filter(tipo="Operador").count()

        return JsonResponse({
            "noturnos": {
                "quantidade": noturnos.count(),
                "colaboradores": list(noturnos.values("nome", "matricula"))
            },
            "vespertinos": {
                "quantidade": vespertinos.count(),
                "colaboradores": list(vespertinos.values("nome", "matricula"))
            },
            "matutinos": {
                "quantidade": matutinos.count(),
                "colaboradores": list(matutinos.values("nome", "matricula"))
            },
            "quantidade_de_motoristas": quantidade_de_motoristas,
            "quantidade_de_coletores": quantidade_de_coletores,
            "quantidade_de_operadores": quantidade_de_operadores
        })

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
      