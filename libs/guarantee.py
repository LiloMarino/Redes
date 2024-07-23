import hashlib
import logging
import re
from pathlib import Path
from socket import socket, timeout

SEPARATOR = b"<<>>"
SECOND_SEPARATOR = b"||"
ENCONDING = "utf-8"


def prepare_data(id: int, payload: bytes) -> bytes:
    header = f"{id}".encode(ENCONDING)
    packet = header + SEPARATOR + payload
    checksum = hashlib.md5(packet).hexdigest().encode("utf-8")
    packet += SEPARATOR + checksum
    return packet


def receive_data(binary_packet: bytes) -> tuple[int, bytes]:
    try:
        parts = binary_packet.split(SEPARATOR)
        if len(parts) != 3:
            raise ValueError("Pacote mal formatado.")

        header, payload, checksum = parts
        if (
            hashlib.md5(header + SEPARATOR + payload).hexdigest().encode(ENCONDING)
            != checksum
        ):
            raise ValueError("Checksum não corresponde.")

        return int(header.decode(ENCONDING)), payload
    except Exception as e:
        raise ValueError(f"Pacote mal formatado.\nPacote:{binary_packet}\nErro:{e}")


def send_basic_data(
    client_socket: socket, ip_port: tuple[str, int], packets_qty: int, file_path: Path
):
    file_name = file_path.name.encode(ENCONDING)
    payload = file_name + SECOND_SEPARATOR + str(packets_qty).encode(ENCONDING)
    binary_packet = prepare_data(0, payload)

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

            # Obtém os dados usando separação de bytes
            parts = payload.split(SECOND_SEPARATOR)
            if len(parts) != 2:
                raise ValueError("Payload mal formatado.")

            file_name, packets_qty = parts
            return file_name.decode(ENCONDING), int(packets_qty.decode(ENCONDING))
        except ValueError as e:
            logging.error("Informações básicas corrompidas, solicitando reenvio...")
            logging.info("Erro: %s", e)
        except Exception as e:
            logging.exception("Erro ao processar dados: %s", e)
