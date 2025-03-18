import json
import logging
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from .models import Veiculo, validar_prefixo, validar_placa, validar_motivo_inatividade

@csrf_exempt
@require_http_methods(["POST"])
def criar_veiculo(request):
    try:
        data = json.loads(request.body)  

        tipos_validos = ["Baú", "Seletolux", "Basculante"]
        if data["tipo"] not in tipos_validos:
            return JsonResponse({"erro": "Tipo de veIculo errado."}, status=400)
        try:
            validar_prefixo(data["prefixo"], data["tipo"])
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=400)
        try:
            validar_placa(data["placa"])
        except ValidationError as e:
            return JsonResponse({"erro": str(e)}, status=400)

        status = data["status"]
        motivo_inatividade = data.get("motivo_inatividade")
        if status == "Inativo":
            if not motivo_inatividade:
                return JsonResponse({"erro": "Motivo de inatividade é obrigatório quando o status é 'Inativo'."}, status=400)
            try:
                validar_motivo_inatividade(motivo_inatividade, status)
            except ValidationError as e:
                return JsonResponse({"erro": str(e)}, status=400)
        else:
            motivo_inatividade = None 
        if Veiculo.objects.filter(placa=data["placa"]).exists():
            return JsonResponse({"erro": "placa ja cadastrada."}, status=400)
        veiculo = Veiculo.objects.create(
            placa=data["placa"],
            tipo=data["tipo"],
            prefixo=data["prefixo"],
            status=data["status"],
            motivo_inatividade=data.get("motivo_inatividade", "")
        )
        return JsonResponse({"mensagem": f"veiculo criado com sucesso: {veiculo.prefixo}"}, status=201)
    
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)



@csrf_exempt
@require_http_methods(["DELETE"])
@require_http_methods(["DELETE"])
def deletar_veiculo(request, placa):
    try:
        _ = request.method 
        veiculo = Veiculo.objects.get(placa=placa) 
        veiculo.delete()
        return JsonResponse({"mensagem": f"veiculo com placa {placa} deletado com sucesso."})
    except Veiculo.DoesNotExist:
        return JsonResponse({"erro": f"veiculo com placa {placa} não encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
    

@csrf_exempt
@require_http_methods(["PUT"])
def editar_veiculo(request,placa):
    try:
        data = json.loads(request.body)
        veiculo = Veiculo.objects.get(placa=placa) 
        veiculo.placa = data["placa"]
        veiculo.tipo = data["tipo"]
        veiculo.prefixo = data["prefixo"]
        veiculo.status = data["status"]
        veiculo.motivo_inatividade = data.get("motivo_inatividade", "")
        veiculo.save()
        return JsonResponse({"mensagem": f"veiculo de plaxa {veiculo.placa} atualizado com sucesso"})
    except Veiculo.DoesNotExist:
        return JsonResponse({"erro": f"colaborador de placa {data['placa']} nao encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt    
@require_http_methods(["GET"])
def quantidade_de_veiculos(request):
    try:
        _ = request.method 
        veiculos_queryset = Veiculo.objects.all().values("id", "status", "motivo_inatividade", "tipo")
        df = pd.DataFrame(list(veiculos_queryset))
        total = len(df)  
        
        return JsonResponse({"quantidade_de_veiculos": total})
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["GET"])
def quantidade_de_veiculos_inativos(request):
    try:
        _ = request.method 
        veiculos_inativos = Veiculo.objects.filter(status="Inativo").values("status","tipo","motivo_inatividade")
        if not veiculos_inativos:
            return JsonResponse({"erro": "nenhum veiculo inativo encontrado."}, status=404)
        df = pd.DataFrame(list(veiculos_inativos))
        logger.info(f"valores unicos de motivo_inatividade: {df['motivo_inatividade'].unique()}")
        if df["motivo_inatividade"].isnull().any():
            logger.warning("existem veiculos inativos sem motivo de inatividade definido.")
        df["motivo_inatividade"] = df["motivo_inatividade"].str.strip().str.lower()
        total_inativos = df.shape[0]
        total_na_garagem = df[df["motivo_inatividade"] == "na garagem"].shape[0]
        total_em_manutencao = df[df["motivo_inatividade"] == "em manutenção"].shape[0]
        tipos_inativos = df["tipo"].value_counts().to_dict()
        logger.info(f"Total inativos: {total_inativos}, Na garagem: {total_na_garagem}, em manutencao: {total_em_manutencao}")
        return JsonResponse({
            "total_inativos": total_inativos,
            "na_garagem": total_na_garagem,
            "em_manutencao": total_em_manutencao,
            "inativos_por_tipo": tipos_inativos
        })
    except Exception as e:
        logger.error(f"erro na funcao 'quantidade_de_veiculos_inativos': {str(e)}")
        return JsonResponse({"erro": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def quantidade_de_veiculos_ativos(request):
    try:
        _ = request.method 
        veiculos_ativos = Veiculo.objects.filter(status="Ativo").values("status", "tipo")
        df = pd.DataFrame(list(veiculos_ativos))
        total_ativos = df.shape[0]
        tipos_ativos = df["tipo"].value_counts().to_dict()
        return JsonResponse({
            "total_ativos": total_ativos,
            "ativos_por_tipo": tipos_ativos
        })
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)
@csrf_exempt
@require_http_methods(["GET"])
def retorna_detalhes_veiculos(request):
    try:
        _ = request.method 
        infos_importantes = Veiculo.objects.values("placa","prefixo","tipo", "status", "motivo_inatividade")
        df = pd.DataFrame(list(infos_importantes))
        return JsonResponse(df.to_dict(orient="records"), safe=False)
    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)