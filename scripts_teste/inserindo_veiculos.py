import requests
import random
import string
import re
import time
from itertools import product
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8000/veiculos/criar/"

NUM_VEICULOS = 100  
MAX_THREADS = 10    

TIPOS_VEICULO = {
    "Baú": "BAÚ",
    "Seletolux": "SL",
    "Basculante": "BS",
}

def buscar_placas_existentes():
    """ Busca as placas já cadastradas para evitar duplicação. """
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return {veiculo["placa"] for veiculo in response.json()}
        else:
            print(f"⚠️ Erro ao buscar placas existentes: {response.status_code}")
            return set()
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erro na requisição: {e}")
        return set()

def gerar_placa(existentes):
    """ Gera uma placa única, evitando duplicadas. """
    padrao_novo = r"^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$"
    padrao_antigo = r"^[A-Z]{3}-[0-9]{4}$"

    while True:
        placa = (
            f"{''.join(random.choices(string.ascii_uppercase, k=3))}{random.randint(0, 9)}{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}"
            if random.choice([True, False])
            else f"{''.join(random.choices(string.ascii_uppercase, k=3))}-{random.randint(1000, 9999)}"
        )
        if placa not in existentes and (re.match(padrao_novo, placa) or re.match(padrao_antigo, placa)):
            existentes.add(placa)
            return placa

def gerar_combinacoes_unicas():
    """ Gera combinações únicas de tipos de veículos. """
    combinacoes = list(TIPOS_VEICULO.keys())
    random.shuffle(combinacoes)
    return combinacoes

def gerar_veiculo(existentes, combinacoes_usadas):
    """ Gera um veículo sempre com status inativo e motivo 'Em manutenção'. """
    while True:
        if not combinacoes_usadas:
            print("⚠️ Todas as combinações foram usadas. Repetindo algumas para atingir o limite!")
            combinacoes_usadas.update(gerar_combinacoes_unicas())

        tipo = combinacoes_usadas.pop()
        prefixo = TIPOS_VEICULO[tipo]

        veiculo = {
            "placa": gerar_placa(existentes),
            "tipo": tipo,
            "prefixo": prefixo,
            "status": "Inativo",  # Sempre inativo
            "motivo_inatividade": "Em manutenção"  # Sempre em manutenção
        }

        return veiculo

def cadastrar_veiculo(veiculo):
    """ Envia o veículo para cadastro na API. """
    try:
        response = requests.post(API_URL, json=veiculo, timeout=5)
        if response.status_code == 201:
            print(f"✅ {veiculo['placa']} cadastrado com sucesso!")
        else:
            print(f"❌ Erro {response.status_code} ao cadastrar {veiculo['placa']}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Falha na requisição para {veiculo['placa']}: {e}")

def cadastrar_veiculos():
    """ Controla o processo de geração e envio dos veículos. """
    existentes = buscar_placas_existentes()  
    combinacoes_usadas = set(gerar_combinacoes_unicas())  

    veiculos = [gerar_veiculo(existentes, combinacoes_usadas) for _ in range(NUM_VEICULOS)]
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(cadastrar_veiculo, veiculos)

if __name__ == "__main__":
    start = time.time()
    cadastrar_veiculos()
    print(f"\n🚀 Cadastro concluído em {time.time() - start:.2f} segundos!")
