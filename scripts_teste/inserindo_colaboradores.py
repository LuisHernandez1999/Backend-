import requests
import random
import concurrent.futures

API_URL = "http://127.0.0.1:8000/colaborador/api/criar/"

nomes = ["Carlos", "Maria", "José", "Ana", "Paulo", "Fernanda", "Lucas", "Juliana", "Rafael", "Camila"]
sobrenomes = ["Silva", "Souza", "Santos", "Oliveira", "Pereira", "Costa", "Rodrigues", "Martins", "Barbosa", "Ferreira"]

pas = ["1", "2", "3", "4"]
turnos = ["Matutino", "Vespertino", "Noturno"]
tipos = ["Motorista", "Coletor", "Operador"]

matriculas_geradas = set()
NUM_COLABORADORES = 2000

# Criar lista de colaboradores antes de enviar para evitar processamento extra
colaboradores = []
for _ in range(NUM_COLABORADORES):
    nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"

    while True:
        matricula = str(random.randint(1000, 9999))
        if matricula not in matriculas_geradas:
            matriculas_geradas.add(matricula)
            break  

    colaboradores.append({
        "nome": nome_completo,
        "matricula": matricula,
        "pa": random.choice(pas),
        "turno": random.choice(turnos),
        "tipo": random.choice(tipos),
    })


def cadastrar_colaborador(colaborador):
    """Função para enviar requisições"""
    response = requests.post(API_URL, json=colaborador)

    if response.status_code == 201:
        print(f"✅ {colaborador['nome']} (Matrícula {colaborador['matricula']}) cadastrado com sucesso!")
    else:
        print(f"❌ Erro ao cadastrar {colaborador['nome']}: {response.text}")


# Usar múltiplas threads para enviar as requisições ao mesmo tempo
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(cadastrar_colaborador, colaboradores)
