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


def host(server_port: int):
    try:
        server_ip = get_local_ip()
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

                # Inicia uma nova thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=cliente, args=(client_socket, ip_cliente)
                )
                client_thread.start()

                # Inicia uma thread para enviar mensagens ao cliente
                send_thread = threading.Thread(
                    target=enviar_mensagem, args=(client_socket,)
                )
                send_thread.start()

    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")


def enviar_mensagem(client_socket: socket):
    while True:
        try:
            mensagem = input("")
            client_socket.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break


def cliente(client_socket: socket, ip_client: str):
    with client_socket:
        while True:
            try:
                # Recebe dados do cliente
                data = client_socket.recv(4096)
                if not data:
                    break

                print("Mensagem recebida: ", data.decode(), " do cliente: ", ip_client)

            except Exception as e:
                print("Erro ao receber dados do cliente ", ip_client, " e ", e)
                break
