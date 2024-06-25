import threading
from socket import *


def client(server_ip: str, server_port: int):
    try:
        print(f"Tentando conexão ao servidor {server_ip}:{server_port}")
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            # Conecta ao servidor
            client_socket.connect((server_ip, server_port))
            print(f"Conectado ao servidor {server_ip}:{server_port}")

            # Inicia thread para receber mensagens do servidor
            receive_thread = threading.Thread(
                target=receber_mensagem, args=(client_socket,)
            )
            receive_thread.start()

            # Loop para enviar mensagens para o servidor
            while True:
                mensagem = input("")
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
            print(f"<>: '{data.decode()}'")
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break
