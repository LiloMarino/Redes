from libs import tester_tcp, tester_udp
from libs.autoload import load_config, save_config

if __name__ == "__main__":
    # Carrega as configurações
    config = load_config()
    option = input("Download (D) ou Upload (U):\n>").upper()

    # Exige o tipo de conexão (TCP/UDP)
    while True:
        protocolo = input(
            f"Digite o protocolo (TCP/UDP) (Default: {config.get('protocolo', '')}):\n>"
        ).strip().upper() or config.get("protocolo", "")
        if protocolo in ("TCP", "UDP"):
            break
        print("Protocolo Inválido!")

    # Seleciona a opção
    while True:
        if option == "D":
            # Exige a port
            server_port = input(
                f"Digite a porta do servidor (Default: {config.get('server_port', 5001)}): "
            ).strip()
            server_port = (
                int(server_port) if server_port else config.get("server_port", 5001)
            )
            # Salva os dados
            config["server_port"] = server_port
            config["protocolo"] = protocolo
            save_config(config)

            # Hospeda
            if protocolo == "TCP":
                tester_tcp.download(server_port)
            else:
                tester_udp.download(server_port, server_port)
        elif option == "U":
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
            config["server_ip"] = server_ip
            config["server_port"] = server_port
            config["protocolo"] = protocolo
            save_config(config)

            # Conecta
            if protocolo == "TCP":
                tester_tcp.upload(server_ip, server_port)
            else:
                tester_udp.upload(server_ip, server_port, server_port)
        else:
            option = input("Opção inválida digite novamente: ").upper()
