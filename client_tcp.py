import os
import re
import threading
from socket import *


def client(server_ip: str, server_port: int, nickname: str):
    try:
        print(f"Tentando conexão ao servidor {server_ip}:{server_port}")
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            # Conecta ao servidor
            client_socket.connect((server_ip, server_port))
            os.system("cls")
            print(f"Conectado ao servidor {server_ip}:{server_port}")

            # Envia o nickname ao servidor
            client_socket.sendall(nickname.encode())

            # Inicia thread para receber mensagens do servidor
            receive_thread = threading.Thread(
                target=receber_mensagem, args=(client_socket,)
            )
            receive_thread.start()

            # Loop para enviar mensagens para o servidor
            while True:
                mensagem = input()
                if mensagem.lower() == "exit":
                    print("Encerrando conexão...")
                    break
                client_socket.sendall(mensagem.encode())
    except Exception as e:
        print(f"Erro ao se conectar ao servidor: {e}")


def receber_mensagem(client_socket: socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            mensagem = data.decode()
            if re.match(r"^SERVER: *", mensagem):
                print(re.sub(r"^SERVER: *", "", mensagem))
            else:
                nickname = re.search(r"^<(.*?)>:", mensagem).group(1)
                print(f"<{nickname}>: {re.sub(r"^<(.*?)>:", "", mensagem)}")
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break
