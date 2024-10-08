import os
import re
import time
from socket import AF_INET, SOCK_STREAM, socket

from tqdm import tqdm

from libs.host_tcp import get_local_ip


def download(server_port: int):
    try:
        server_ip = get_local_ip()

        with socket(AF_INET, SOCK_STREAM) as host_socket:
            host_socket.bind((server_ip, server_port))
            host_socket.listen(1)
            print(f"Hospedando em {server_ip}:{server_port}\n")

            client_socket, ip_cliente = host_socket.accept()
            total_bytes = 0
            total_pacotes = 0
            tempo_inicial = time.time()

            with tqdm(total=20, desc="Recebendo dados", unit="s", ncols=100) as pbar:
                while True:
                    data = client_socket.recv(500)
                    if not data or b"END" in data:
                        break
                    total_bytes += len(data)
                    total_pacotes += 1
                    tempo_atual = time.time()
                    pbar.update(tempo_atual - tempo_inicial - pbar.n)
                    if tempo_atual - tempo_inicial >= 20:
                        break

            # Consome o buffer até encontrar "END"
            while data and b"END" not in data:
                data = client_socket.recv(500)

            match = re.search(r"END(\d+)", data.decode())
            total_pacotes_enviados = int(match.group(1))

            client_socket.close()

            # Calcula os pacotes perdidos
            if total_pacotes_enviados < total_pacotes:
                total_pacotes = total_pacotes_enviados
            pacotes_perdidos = total_pacotes_enviados - total_pacotes
            tempo_total = time.time() - tempo_inicial
            taxa_transferencia_bps = (total_bytes * 8) / tempo_total
            pacotes_por_segundo = total_pacotes / tempo_total

            print(f"Conexão encerrada com {ip_cliente}")
            print(f"Total de bytes recebidos: {total_bytes:,}")
            print(f"Total de pacotes recebidos: {total_pacotes:,}")
            print(f"Total de pacotes enviados: {total_pacotes_enviados:,}")
            print(f"Total de pacotes perdidos: {pacotes_perdidos:,}")
            print(
                f"""Taxa de transferência:
                  {taxa_transferencia_bps / 1e9:,.2f} Gbit/s
                  {taxa_transferencia_bps / 1e6:,.2f} Mbit/s
                  {taxa_transferencia_bps / 1e3:,.2f} Kbit/s
                  {taxa_transferencia_bps:,.2f} bit/s
                """
            )
            print(f"Pacotes por segundo: {pacotes_por_segundo:,.2f} pacotes/s")
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")


def upload(server_ip: str, server_port: int):
    try:
        print(f"Tentando conexão ao servidor {server_ip}:{server_port}")
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            os.system("cls")
            print(f"Conectado ao servidor {server_ip}:{server_port} via TCP")

            mensagem_base = "teste de rede *2024*"
            mensagem = (mensagem_base * (500 // len(mensagem_base)))[:500]

            total_bytes = 0
            total_pacotes = 0
            tempo_inicial = time.time()

            with tqdm(total=20, desc="Enviando dados", unit="s", ncols=100) as pbar:
                while True:
                    client_socket.sendall(mensagem.encode())
                    total_bytes += len(mensagem)
                    total_pacotes += 1
                    tempo_atual = time.time()
                    pbar.n = min(20, tempo_atual - tempo_inicial)
                    pbar.refresh()  # Atualiza a barra de progresso
                    if tempo_atual - tempo_inicial >= 20:
                        break

            # Envia "END" e o total de pacotes enviados
            client_socket.sendall("END".encode())
            client_socket.sendall(str(total_pacotes).encode())

            tempo_total = time.time() - tempo_inicial
            taxa_transferencia_bps = (total_bytes * 8) / tempo_total
            pacotes_por_segundo = total_pacotes / tempo_total

            print(f"Conexão encerrada com o servidor {server_ip}:{server_port}")
            print(f"Total de bytes enviados: {total_bytes:,}")
            print(f"Total de pacotes enviados: {total_pacotes:,}")
            print(
                f"""Taxa de transferência:
                  {taxa_transferencia_bps / 1e9:,.2f} Gbit/s
                  {taxa_transferencia_bps / 1e6:,.2f} Mbit/s
                  {taxa_transferencia_bps / 1e3:,.2f} Kbit/s
                  {taxa_transferencia_bps:,.2f} bit/s
                """
            )
            print(f"Pacotes por segundo: {pacotes_por_segundo:,.2f} pacotes/s")
    except Exception as e:
        print(f"Erro ao se conectar ao servidor: {e}")
