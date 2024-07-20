from libs import client_tcp, client_udp, host_tcp, host_udp
from libs.autoload import load_config, save_config

if __name__ == "__main__":
    # Carrega as configurações
    config = load_config()
    option = input("Hospedar (H) ou Cliente (C):\n>").upper()

    # Exige o tipo de conexão (TCP/UDP)
    while True:
        protocolo = input(
            f"Digite o protocolo (TCP/UDP) (Default: {config.get('protocolo', '')}):\n>"
        ).strip().upper() or config.get("protocolo", "")
        if protocolo in ("TCP", "UDP"):
            break
        print("Protocolo Inválido!")

    # Exige o nick
    while True:
        nickname = input(
            f"Digite um apelido (Default: {config.get('nickname', '')}):\n>"
        ).strip() or config.get("nickname", "")
        if nickname:
            break

    # Seleciona a opção
    while True:
        if option == "H":
            # Exige a port
            server_port = input(
                f"Digite a porta do servidor (Default: {config.get('server_port', 5001)}): "
            ).strip()
            server_port = (
                int(server_port) if server_port else config.get("server_port", 5001)
            )
            # Salva os dados
            config["nickname"] = nickname
            config["server_port"] = server_port
            save_config(config)

            # Hospeda
            if protocolo == "TCP":
                host_tcp.host(server_port, nickname)
            else:
                host_udp.host(server_port, nickname)
        elif option == "C":
            # Exige o ip e a port
            server_ip = input(
                f"Digite o IP do servidor (Default: {config.get('server_ip', '')}): "
            ).strip() or config.get("server_ip", "")
            server_port = input(
                f"Digite a porta do servidor (Default: {config.get('server_port', 5001)}): "
            ).strip()
            server_port = (
                int(server_port) if server_port else config.get("server_port", 5001)
            )

            # Salva os dados
            config["nickname"] = nickname
            config["server_ip"] = server_ip
            config["server_port"] = server_port
            save_config(config)

            # Conecta
            if protocolo == "TCP":
                client_tcp.client(server_ip, server_port, nickname)
            else:
                client_udp.client(server_ip, server_port, nickname)
        else:
            option = input("Opção inválida digite novamente: ").upper()
