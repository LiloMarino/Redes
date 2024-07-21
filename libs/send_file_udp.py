import logging
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket, timeout

from tqdm import tqdm

from libs.guarantee import prepare_data, send_basic_data


def get_packets(file_path: Path, packet_size: int) -> list[bytes]:
    i = 0
    packets = []
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(packet_size)
            if not chunk:
                break
            data = prepare_data(i, chunk)
            packets.append(data)
            i += 1
    return packets


def file_client(server_ip: str, server_port: int, packet_size: int, file_path: Path):
    packets = get_packets(file_path, packet_size)
    number_packets = len(packets)
    try:
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            client_socket.settimeout(
                2
            )  # Adiciona um timeout de 2 segundos para os ACKs
            send_basic_data(
                client_socket, (server_ip, server_port), number_packets, file_path
            )

            for i, packet in enumerate(tqdm(packets, desc="Enviando", unit="pacote")):
                while True:
                    client_socket.sendto(packet, (server_ip, server_port))
                    try:
                        ack, _ = client_socket.recvfrom(1024)
                        if ack == b"ACK":
                            break
                        else:
                            logging.info("ACK não recebido, reenviando pacote ID:%s", i)
                    except timeout:
                        logging.info(
                            "Tempo esgotado esperando ACK, reenviando pacote ID:%s", i
                        )
            print("Arquivo enviado com sucesso!")
    except Exception as e:
        print(f"Erro no cliente: {e}")
