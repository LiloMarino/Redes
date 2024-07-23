import hashlib
import logging
import re
from pathlib import Path
from socket import socket, timeout

SEPARATOR = "<>"
SECOND_SEPARATOR = "||"
ENCONDING = "utf-8"


def prepare_data(id: int, payload: bytes) -> bytes:
    header = f"{id}"
    packet = f"{header}{SEPARATOR}".encode(encoding=ENCONDING) + payload
    checksum = hashlib.md5(packet).hexdigest()
    packet += f"{SEPARATOR}{checksum}".encode(encoding=ENCONDING)
    return packet


def receive_data(binary_packet: bytes) -> tuple[int, bytes]:
    packet = binary_packet.decode(encoding=ENCONDING)
    pattern = rf"^(\d+){re.escape(SEPARATOR)}(.+){re.escape(SEPARATOR)}([a-fA-F0-9]+)$"
    match = re.match(pattern, packet)
    if match:
        header, payload, checksum = match.groups()
        payload = payload.encode(encoding=ENCONDING)
        if (
            hashlib.md5(
                f"{header}{SEPARATOR}".encode(encoding=ENCONDING) + payload
            ).hexdigest()
            == checksum
        ):
            return int(header), payload
        else:
            raise ValueError(
                f"Pacote corrompido\nHeader:{header}\nPayload:{payload}\nChecksum{checksum}"
            )
    else:
        raise ValueError(f"Pacote mal formatado.\nPacote:{packet}")


def send_basic_data(
    client_socket: socket, ip_port: tuple[str, int], packets_qty: int, file_path: Path
):
    file_name = file_path.name
    payload = f"{file_name}{SECOND_SEPARATOR}{packets_qty}"
    binary_packet = prepare_data(0, payload.encode(ENCONDING))

    while True:
        client_socket.sendto(binary_packet, ip_port)
        try:
            data, _ = client_socket.recvfrom(4096)
            if data:
                print("Enviado informações básicas com sucesso!")
                break
        except timeout:
            logging.info(
                "Tempo esgotado esperando ACK, reenviando informações básicas..."
            )
        except Exception as e:
            logging.exception("Erro ao receber ACK: %s", e)
            logging.info("Tentando reenviar...")


def receive_basic_data(server_socket: socket):
    while True:
        try:
            data, receive_address = server_socket.recvfrom(4096)
            header, payload = receive_data(data)

            # Envia ACK para confirmar o recebimento
            server_socket.sendto(b"ACK", receive_address)

            # Obtém os dados usando expressões regulares
            pattern = rf"^(.+){re.escape(SECOND_SEPARATOR)}(.+)$"
            match = re.match(pattern, payload.decode(encoding=ENCONDING))
            if match:
                file_name, packets_qty = match.groups()
                return file_name, int(packets_qty)
            else:
                logging.error("Erro ao processar o payload.")
                logging.info("PAYLOAD: %s", payload)
        except ValueError:
            logging.error("Informações básicas corrompidas, solicitando reenvio...")
        except Exception as e:
            logging.exception("Erro ao processar dados: %s", e)
