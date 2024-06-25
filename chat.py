option = input("Hospedar (H) ou Cliente (C)").upper()

while True:
    if option == "H":
        host()
    elif option == "C":
        client()
    else:
        option = input("Opção inválida digite novamente:").upper()
