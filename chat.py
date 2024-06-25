from autoload import load_config, save_config
from client_tcp import client
from host_tcp import host

if __name__ == "__main__":
    # Carrega as configurações
    config = load_config()
    option = input("Hospedar (H) ou Cliente (C):\n>").upper()

    # Exige o nick
    nickname = input(
        f"Digite um apelido (Default: {config.get('nickname', '')}):\n>"
        or {config.get("nickname", "")}
    ).strip()
    
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
            host(server_port)
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
            client(server_ip, server_port)
        else:
            option = input("Opção inválida digite novamente: ").upper()
