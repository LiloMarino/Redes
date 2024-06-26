import threading
from socket import *


def get_local_ip():
    try:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Não foi possível obter o IP local: {e}")
        return "127.0.0.1"  # Fallback para loopback


def host(server_port: int, host_nickname: str):
    try:
        server_ip = get_local_ip()
        nicknames = {}
        with socket(AF_INET, SOCK_STREAM) as host_socket:
            # Liga o socket à porta local
            host_socket.bind((server_ip, server_port))

            # Define o socket para escutar até 5 conexões simultâneas
            host_socket.listen(5)
            print(f"Hospedando em {server_ip}:{server_port}\n")

            while True:
                # Aceita conexões dos clientes
                client_socket, ip_cliente = host_socket.accept()
                print("Conexão estabelecida com ", ip_cliente)

                # Recebe o nickname do cliente
                nickname = client_socket.recv(1024).decode()
                nicknames[client_socket] = nickname
                joined_server(nickname, client_socket)

                # Inicia uma nova thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=cliente, args=(client_socket, ip_cliente, nicknames)
                )
                client_thread.start()

                # Inicia uma thread para enviar mensagens ao cliente
                send_thread = threading.Thread(
                    target=enviar_mensagem, args=(client_socket, host_nickname)
                )
                send_thread.start()

    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")


def joined_server(nickname: str, client_socket: socket):
    client_socket.sendall(f"SERVER: {nickname} entrou no servidor!".encode())


def left_server(nickname: str, client_socket: socket):
    client_socket.sendall(f"SERVER: {nickname} saiu do servidor!".encode())


def enviar_mensagem(client_socket: socket, host_nickname: str):
    while True:
        try:
            mensagem = f"<{host_nickname}>:" + input()
            client_socket.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break


def cliente(client_socket: socket, ip_client: str, nicknames: dict):
    with client_socket:
        nickname = nicknames[client_socket]
        try:
            while True:
                # Recebe dados do cliente
                data = client_socket.recv(4096)
                if not data:
                    left_server(nickname, client_socket)
                    break
                print(f"<{nickname}>: {data.decode()}")

        except Exception as e:
            print(f"Erro ao receber dados do cliente {nickname} ({ip_client}): {e}")
