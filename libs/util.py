import time
from socket import AF_INET, SOCK_STREAM, socket

from libs.host_tcp import get_local_ip


def receive_lost_packet(server_port: int) -> int:
    try:
        server_ip = get_local_ip()
        with socket(AF_INET, SOCK_STREAM) as host_socket:
            host_socket.bind((server_ip, server_port))
            host_socket.listen(1)
            client_socket, ip_cliente = host_socket.accept()
            with client_socket:
                data = client_socket.recv(500)
                return int(data.decode())
    except Exception as e:
        print(f"Erro ao receber pacotes perdidos: {e}")
        return -1  # Retorne um valor de erro apropriado


def send_lost_packet(server_ip: str, server_port: int, lost_packets: int):
    time.sleep(3)
    try:
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.sendall(str(lost_packets).encode())
    except Exception as e:
        print(f"Erro ao enviar pacotes perdidos: {e}")
