import hashlib
import re
from pathlib import Path
from socket import socket

SEPARATOR = "<>"
SECOND_SEPARATOR = "||"


def prepare_data(id: int, payload: str | bytes) -> bytes:
    header = f"{id}"
    packet = f"{header}{SEPARATOR}{payload}"
    checksum = hash(packet)
    packet = f"{packet}{SEPARATOR}{checksum}"
    binary_packet = packet.encode()
    return binary_packet


def receive_data(binary_packet: bytes) -> tuple[int, str | bytes]:
    packet = binary_packet.decode()
    # Expressão regular para obter os dados do pacote
    pattern = rf"^(\d+){SEPARATOR}(.+){SEPARATOR}(\d+)$"
    match = re.match(pattern, packet)
    if match:
        header, payload, checksum = match.groups()
        # Verifica se o checksum é válido
        if hash(f"{header}{SEPARATOR}{payload}") == checksum:
            return (int(header), payload)
        else:
            raise ValueError("Pacote corrompido")
    else:
        raise ValueError("Pacote mal formatado")


def send_basic_data(
    client_socket: socket, ip_port: tuple[str, str], packets_qty: int, file_path: Path
):
    file_name = file_path.name
    payload = f"{file_name}{SECOND_SEPARATOR}{packets_qty}"
    binary_packet = prepare_data(0, payload)
    # Realiza uma tentativa de envio e caso não dê certo reenvia
    data = None
    while data != b"ACK":
        client_socket.sendto(binary_packet, ip_port)
        data, _ = client_socket.recvfrom(4096)
    print("Enviado informações básicas com sucesso!")


def receive_basic_data(server_socket: socket):
    # Recebe o pacote com as informações básicas
    payload = None
    retry = True
    while retry:
        data, receive_address = server_socket.recvfrom(4096)
        try:
            _, payload = receive_data(data)
            retry = False
            # Envia ACK para confirmar o recebimento
            server_socket.sendto(b"ACK", receive_address)
        except ValueError:
            print("Pacote corrompido, solicitando reenvio...")
            server_socket.sendto(b"NOT", receive_address)

    # Obtém os dados usando expressões regulares
    pattern = rf"^(.+){SECOND_SEPARATOR}(.+)$"
    match = re.match(pattern, payload)
    if match:
        file_name, packets_qty = match.groups()
        return file_name, packets_qty
    else:
        raise ValueError("Erro ao obter dados básicos")


def hash_with_seed(data: bytes, seed: bytes) -> str:
    # Combine a semente com os dados
    combined_data = seed + data
    # Crie um hash SHA-256
    hash_object = hashlib.sha256(combined_data)
    # Retorne o hash como uma string hexadecimal
    return hash_object.hexdigest()
