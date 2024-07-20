import os
import re
import threading
from socket import AF_INET, SOCK_DGRAM, socket


def client(server_ip: str, server_port: int, nickname: str):
    try:
        print(f"Tentando conexão ao servidor {server_ip}:{server_port}")
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            os.system("cls")
            print(f"Conectado ao servidor {server_ip}:{server_port} via UDP")

            # Envia o nickname ao servidor
            client_socket.sendto(nickname.encode(), (server_ip, server_port))

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
                client_socket.sendto(mensagem.encode(), (server_ip, server_port))
    except Exception as e:
        print(f"Erro ao se conectar ao servidor: {e}")


def receber_mensagem(client_socket: socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            if not data:
                break
            mensagem = data.decode()
            if re.match(r"^SERVER: *", mensagem):
                print(re.sub(r"^SERVER: *", "", mensagem))
            else:
                nickname_match = re.search(r"^<(.*?)>:", mensagem)
                if nickname_match:
                    nickname = nickname_match.group(1)
                    print(f"<{nickname}>: {mensagem[len(nickname)+3:]}")
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break
