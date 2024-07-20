import threading
from socket import AF_INET, SOCK_DGRAM, socket

from libs.host_tcp import get_local_ip


def host(server_port: int, host_nickname: str):
    try:
        server_ip = get_local_ip()
        nicknames = {}

        # Inicia uma thread para enviar mensagens aos clientes:
        send_thread = threading.Thread(
            target=enviar_mensagem, args=(nicknames, host_nickname)
        )
        send_thread.start()

        with socket(AF_INET, SOCK_DGRAM) as host_socket:
            # Liga o socket à porta local em qualquer IP
            host_socket.bind(("", server_port))
            print(f"Hospedando em {server_ip}:{server_port}\n")

            while True:
                # Recebe dados do cliente
                data, ip_cliente = host_socket.recvfrom(1024)
                nickname = data.decode()
                nicknames[nickname] = ip_cliente
                for client in nicknames.values():
                    joined_server(nickname, host_socket, client)

                # Inicia uma nova thread para escutar o cliente
                client_thread = threading.Thread(
                    target=escutar_cliente,
                    args=(nickname, nicknames, host_socket),
                )
                client_thread.start()

    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")


def joined_server(nickname: str, host_socket: socket, client_addr):
    host_socket.sendto(f"SERVER: {nickname} entrou no servidor!".encode(), client_addr)


def left_server(nickname: str, host_socket: socket, client_addr):
    host_socket.sendto(f"SERVER: {nickname} saiu do servidor!".encode(), client_addr)


def enviar_mensagem(nicknames: dict[str, tuple], host_nickname: str):
    try:
        while True:
            mensagem = f"<{host_nickname}>:" + input()
            for client_addr in nicknames.values():
                with socket(AF_INET, SOCK_DGRAM) as send_socket:
                    send_socket.sendto(mensagem.encode(), client_addr)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")


def escutar_cliente(nickname: str, nicknames: dict[str, tuple], host_socket: socket):
    client_addr = nicknames[nickname]
    try:
        while True:
            # Recebe dados do cliente
            data, _ = host_socket.recvfrom(4096)
            if not data:
                break
            mensagem = f"<{nickname}>:{data.decode()}"
            print(mensagem)
            for client in nicknames.values():
                if client != client_addr:
                    host_socket.sendto(mensagem.encode(), client)

    except Exception as e:
        print(f"Erro ao receber dados do cliente {nickname}: {e}")

    finally:
        # Remove o cliente e a thread associada ao desconectar
        del nicknames[nickname]
        for client in nicknames.values():
            left_server(nickname, host_socket, client)
        print(f"{nickname} saiu do servidor!")
