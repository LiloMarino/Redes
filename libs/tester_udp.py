import os
import time
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket

from tqdm import tqdm

from libs.host_tcp import get_local_ip


def download(server_port: int, tcp_port: int):
    try:
        server_ip = get_local_ip()

        with socket(AF_INET, SOCK_DGRAM) as host_socket:
            host_socket.bind(("", server_port))
            print(f"Hospedando em {server_ip}:{server_port} para UDP\n")

            total_bytes = 0
            total_pacotes = 0
            total_pacotes_enviados = 0
            tempo_inicial = time.time()

            with tqdm(total=20, desc="Recebendo dados", unit="s", ncols=100) as pbar:
                while True:
                    data, ip_cliente = host_socket.recvfrom(500)
                    total_bytes += len(data)
                    total_pacotes += 1

                    tempo_atual = time.time()
                    pbar.update(tempo_atual - tempo_inicial - pbar.n)
                    if tempo_atual - tempo_inicial >= 20:
                        break

            # Após o tempo limite, receber o total de pacotes via TCP
            with socket(AF_INET, SOCK_STREAM) as tcp_socket:
                tcp_socket.bind(("", tcp_port))
                tcp_socket.listen(1)
                print(f"Hospedando em {server_ip}:{tcp_port} para TCP\n")
                conn, addr = tcp_socket.accept()
                with conn:
                    total_pacotes_enviados = int(conn.recv(1024).decode())

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


def upload(server_ip: str, server_port: int, tcp_port: int):
    try:
        print(f"Tentando conexão ao servidor {server_ip}:{server_port}")
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            os.system("cls")
            print(f"Conectado ao servidor {server_ip}:{server_port} via UDP")

            mensagem_base = "teste de rede *2024*"
            mensagem = (mensagem_base * (500 // len(mensagem_base)))[:500]

            total_bytes = 0
            total_pacotes = 0
            tempo_inicial = time.time()

            with tqdm(total=20, desc="Enviando dados", unit="s", ncols=100) as pbar:
                while True:
                    client_socket.sendto(mensagem.encode(), (server_ip, server_port))
                    total_bytes += len(mensagem)
                    total_pacotes += 1
                    tempo_atual = time.time()
                    pbar.n = min(20, tempo_atual - tempo_inicial)
                    pbar.refresh()
                    if tempo_atual - tempo_inicial >= 20:
                        break

            # Envia o total de pacotes via TCP para garantir a entrega
            with socket(AF_INET, SOCK_STREAM) as tcp_socket:
                tcp_socket.connect((server_ip, tcp_port))
                tcp_socket.sendall(f"{total_pacotes}".encode())

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
