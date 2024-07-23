import locale
import logging
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from libs.autoload import load_config, save_config
from libs.receive_file_udp import file_server
from libs.send_file_udp import file_client

logging.basicConfig(
    format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("info.log", "w", "utf-8"),
    ],
)
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def format_number(number):
    return locale.format_string("%d", number, grouping=True)


if __name__ == "__main__":
    # Inicializa a janela Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Carrega as configurações
    config = load_config()
    option = input("Receber (R) ou Enviar (E):\n>").upper()

    # Seleciona a opção
    while True:
        if option == "R":
            # Exige a port
            server_port = input(
                f"Digite a porta do servidor (Default: {config.get('server_port', 5001)}): "
            ).strip() or config.get("server_port", 5001)
            server_port = int(server_port)

            # Salva os dados
            config["server_port"] = server_port
            save_config(config)

            # Recebe o arquivo
            file_server(server_port)
            break
        elif option == "E":
            # Exige o ip e a port
            server_ip = input(
                f"Digite o IP do servidor (Default: {config.get('server_ip', '')}): "
            ).strip() or config.get("server_ip", "")
            server_port = input(
                f"Digite a porta do servidor (Default: {config.get('server_port', 5001)}): "
            ).strip() or config.get("server_port", 5001)
            server_port = int(server_port)
            packet_size = input(
                f"Digite o tamanho do pacote (bytes) (Default: {config.get('packet_size', 500)}): "
            ).strip() or config.get("packet_size", 500)
            packet_size = int(packet_size)

            # Salva os dados
            config["server_ip"] = server_ip
            config["server_port"] = server_port
            config["packet_size"] = packet_size
            save_config(config)

            # Exige o arquivo
            path_arquivo = Path(filedialog.askopenfilename(title="Selecione o arquivo"))

            if path_arquivo:
                # Envia o arquivo
                relatorio = file_client(
                    server_ip, server_port, packet_size, path_arquivo
                )

                # Imprimir relatório formatado
                print("Relatório de Transferência:")
                print(
                    f"Tamanho do arquivo: {format_number(relatorio['tamanho'])} bytes"
                )
                print(
                    f"Número de pacotes enviados: {format_number(relatorio['enviados'])}"
                )
                print(
                    f"Número de pacotes perdidos: {format_number(relatorio['perdidos'])}"
                )
                print(
                    f"Velocidade: {format_number(int(relatorio['velocidade']))} bits/s"
                )
                break
            else:
                print("Nenhum arquivo selecionado.")
        else:
            option = input("Opção inválida digite novamente: ").upper()
