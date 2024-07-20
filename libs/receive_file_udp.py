from socket import AF_INET, SOCK_DGRAM, socket

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
            while len(packets) < packets_qty:
                while True:
                    data, sender_address = server_socket.recvfrom(4096)
                    try:
                        header, payload = receive_data(data)
                        packets[header] = payload
                        # Envia o ACK para confirmar o recebimento do pacote
                        server_socket.sendto(b"ACK", sender_address)
                        break
                    except ValueError:
                        # Envia NOT para solicitar o reenvio do pacote corrompido
                        server_socket.sendto(b"NOT", sender_address)

            # Ordena os pacotes com base no header e salva o arquivo no disco
            sorted_packets = [packets[i] for i in sorted(packets.keys(), key=int)]
            with open(file_name, "wb") as file:
                for data in sorted_packets:
                    file.write(data)
            print("Transferência de arquivo concluída.")

    except Exception as e:
        print(f"Erro no servidor: {e}")
