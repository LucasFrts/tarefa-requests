import requests
import time
import mysql.connector

from dotenv import load_dotenv
from os import environ

load_dotenv()

database = str(environ.get("DB_DATABASE"))
user = str(environ.get("DB_USER")) 
password = str(environ.get("DB_PASSWORD"))
host = str(environ.get("DB_HOST"))

db_config = {
    'user': user,
    'password': password,
    'host': host,
    'database': database
}

url = 'https://dry-field-444.fly.dev/api/user/get-all'

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


while True:
    response = requests.get(url)

    if response.status_code == 200:
        print('<---- Requisição bem-sucedida ---->')
        
        cursor.execute("SELECT * FROM requisicoes WHERE tipo = 'fly.io'")
        existing_record = cursor.fetchone()
        
        if existing_record:
            # Já existe um registro com o tipo "fly.io", adiciona 1 à quantidade
            new_quantity = existing_record[2] + 1
            cursor.execute("UPDATE requisicoes SET quantidade = %s WHERE tipo = 'fly.io'", (new_quantity,))
            conn.commit()
        else:
            cursor.execute("INSERT INTO requisicoes (tipo, quantidade) VALUES ('fly.io', 1)")
            conn.commit()
        print(f"<---- Requisições realizadas: {new_quantity} ---->")
    else:
        print('Erro na requisição')

    time.sleep(15)

cursor.close()
conn.close()
