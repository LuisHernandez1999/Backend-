import os
import psycopg2
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import call_command
from apps.colaborador.models import Colaborador


DB_NAME = os.getenv('DB_NAME', 'coletaseletiva')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'luis27')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')


try:
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"✅ Banco de dados '{DB_NAME}' criado com sucesso.")
    else:
        print(f"📌 Banco de dados '{DB_NAME}' já existe.")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"❌ Erro ao criar banco de dados: {e}")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


def banco_existe():
    try:
        connection = connections['default']
        connection.cursor()
        return True
    except OperationalError:
        return False


if banco_existe():
    print("📌 Aplicando migrações no banco de dados...")
    call_command('migrate')

    if Colaborador.objects.count() == 0:
        print(" criando um colaborador ")
        Colaborador.objects.create(nome="João Silva", matricula="1234", pa="1", turno="Matutino", tipo="Motorista")
    else:
        print("📌 Tabela 'Colaborador' já possui registros.")

print(" banco de dados e tabelas configurados com sucesso!")
