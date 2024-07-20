from pathlib import Path
from tkinter import filedialog

from libs.autoload import load_config, save_config
from libs.receive_file_udp import file_server
from libs.send_file_udp import file_client

if __name__ == "__main__":
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
            packet_size = input(
                f"Digite o tamanho do pacote (bytes) (Default: {config.get('packet_size', 500)}): "
            ).strip() or config.get("packet_size", 500)
            packet_size = int(packet_size)

            # Salva os dados
            config["server_port"] = server_port
            config["packet_size"] = packet_size
            save_config(config)

            # Recebe o arquivo
            file_server(server_port, packet_size)
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
            path_arquivo = Path(filedialog.askopenfilename())

            # Envia o arquivo
            file_client(server_ip, server_port, packet_size, path_arquivo)
        else:
            option = input("Opção inválida digite novamente: ").upper()
