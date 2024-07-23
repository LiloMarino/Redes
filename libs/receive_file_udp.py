import logging
from socket import AF_INET, SOCK_DGRAM, socket

from tqdm import tqdm

from libs.guarantee import receive_basic_data, receive_data
from libs.host_tcp import get_local_ip


def file_server(server_port: int):
    try:
        server_ip = get_local_ip()
        with socket(AF_INET, SOCK_DGRAM) as server_socket:
            # Liga o socket à porta local em qualquer IP
            server_socket.bind(("0.0.0.0", server_port))
            print(f"Receptor UDP de arquivos hospedado em {server_ip}:{server_port}")

            # Recebe os dados básicos do arquivo
            file_name, packets_qty = receive_basic_data(server_socket)
            packets = {}

            # Recebe todos os pacotes
            with tqdm(total=packets_qty, desc="Recebendo", unit="pacote") as pbar:
                while len(packets) < packets_qty:
                    data, sender_address = server_socket.recvfrom(4096)
                    try:
                        header, payload = receive_data(data)
                        packets[header] = payload
                        server_socket.sendto(b"ACK", sender_address)
                        if len(packets) > pbar.n:
                            # Envia o ACK para confirmar o recebimento do pacote
                            pbar.update(1)
                    except ValueError as e:
                        logging.exception("Value Error %s", e)

            with open(file_name, "wb") as file:
                for i in range(packets_qty):
                    file.write(packets[i])
            print("Transferência de arquivo concluída.")

    except Exception as e:
        print(f"Erro no servidor: {e}")
